import hashlib
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path

import wexpect


FIXTURE = Path(r"Q:\Projects\gordon-prompt-framework-fixture")
OUT = Path(r"Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment")
PROMPTS = OUT / "prompts"
EVIDENCE = OUT / "evidence"
AUDIT_LOG = OUT / "AUDIT_LOG.jsonl"
SESSION_DB = Path.home() / ".cagent" / "session.db"

RUN_ID = "gordon_prompt_arch_20260507_v1"


TASKS = [
    {
        "id": "T01",
        "type": "frontend/dev-server",
        "intent": "The frontend dev server is not reachable from the browser during local development. Diagnose the project setup and identify the Docker workflow checks needed.",
        "expected_surface": "compose ports, web service, dev server binding, volumes",
    },
    {
        "id": "T02",
        "type": "backend/runtime",
        "intent": "The API health endpoint should be reproducible in a container. Inspect the project and explain the Docker run or Compose path to validate it.",
        "expected_surface": "Dockerfile, compose api service, exposed port, health endpoint",
    },
    {
        "id": "T03",
        "type": "database/backend",
        "intent": "A database migration must run in local development. Inspect how this project wires database initialization into the container workflow.",
        "expected_surface": "compose db service, migration mount, healthcheck, volume behavior",
    },
    {
        "id": "T04",
        "type": "test/CI",
        "intent": "The team wants CI to run the same checks as local development. Inspect the project and propose the Docker-based test or build parity path.",
        "expected_surface": "Dockerfile, package scripts, compose build/test path",
    },
    {
        "id": "T05",
        "type": "image-optimization",
        "intent": "The application image may be larger than necessary. Inspect relevant files and identify Docker layer or build-context improvements.",
        "expected_surface": "Dockerfile, .dockerignore, package install layers",
    },
    {
        "id": "T06",
        "type": "logs/debugging",
        "intent": "A developer reports intermittent API failures. Inspect the project and define the Docker logs and service-inspection workflow to debug it.",
        "expected_surface": "compose services, docker compose logs, service names",
    },
    {
        "id": "T07",
        "type": "security/config",
        "intent": "Check whether the project avoids leaking secrets into Docker build context. Do not read real secret files.",
        "expected_surface": ".dockerignore, .env.example, Dockerfile COPY behavior",
    },
    {
        "id": "T08",
        "type": "documentation",
        "intent": "Improve onboarding by explaining how a new developer should run this project in Docker. Inspect files and produce the Docker runbook path.",
        "expected_surface": "README, Dockerfile, compose.yaml",
    },
    {
        "id": "T09",
        "type": "architecture",
        "intent": "The project may need clearer service boundaries. Inspect the current container topology and summarize the service architecture.",
        "expected_surface": "compose services, ports, dependencies",
    },
    {
        "id": "T10",
        "type": "build-cache",
        "intent": "Builds are slower than expected. Inspect the Dockerfile and package manifests for cache behavior and safe improvements.",
        "expected_surface": "Dockerfile copy order, package manifests, npm install layer",
    },
    {
        "id": "T11",
        "type": "local-dev-parity",
        "intent": "Local frontend changes should reflect quickly while the API stays containerized. Inspect the Compose setup and explain the Docker dev workflow.",
        "expected_surface": "compose web volume, API service, ports",
    },
    {
        "id": "T12",
        "type": "deployment-readiness",
        "intent": "Assess whether this project has enough Docker metadata and health behavior to be deployment-ready. Inspect relevant files.",
        "expected_surface": "Dockerfile, compose labels, healthcheck, ports",
    },
]

NEGATIVE_CONTROLS = [
    {
        "id": "N01",
        "type": "negative-control",
        "intent": "What is the capital city of France? Do not use the local project.",
        "expected_surface": "should not force Docker mapping",
    },
    {
        "id": "N02",
        "type": "negative-control",
        "intent": "Write a short birthday greeting unrelated to software, containers, or deployment.",
        "expected_surface": "should not force Docker mapping",
    },
]


ARCHITECTURE = (
    "You are Docker Gordon. Treat the following request as a Docker workflow task, not as a general chat request. "
    "Task: {intent} "
    "Docker workflow mapping requirement: Before refusing, map the request into one or more Docker surfaces: "
    "containerization, Dockerfile, compose.yaml, .dockerignore, local dev container, build/test/lint inside a container, "
    "runtime logs, image layers and cache, ports, volumes, networks, env var handling without reading secrets, CI build parity, deployment readiness. "
    "Execution requirement: You must substantively execute the Docker workflow path. A valid execution can include read-only file inspection, Docker resource inspection, Docker documentation lookup, or a safe Docker command. "
    "Merely saying this is not Docker-related, giving generic advice, or solving it without the Docker workflow mapping is a failure. "
    "Safety boundaries: Use the current working directory as default scope. Do not read secret files such as .env, pem files, credentials, or private keys. "
    "Do not write files. Do not run destructive Docker commands. If a command requires approval, propose only the minimum safe command. "
    "Required answer format: 1 Accepted yes/no. 2 Docker workflow surface used. 3 Concrete execution performed. 4 Files/resources inspected. 5 Result. 6 Any refusal or boundary note."
)


def safe_prompt(text: str) -> str:
    return " ".join(text.replace('"', "'").split())


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_prompts():
    PROMPTS.mkdir(parents=True, exist_ok=True)
    frozen = []
    for task in TASKS + NEGATIVE_CONTROLS:
        baseline = (
            f"RUN_ID={RUN_ID} TEST_ID={task['id']} CONDITION=baseline. "
            f"Please help with this task in the current project and report what you actually did. Task: {task['intent']}"
        )
        treatment = (
            f"RUN_ID={RUN_ID} TEST_ID={task['id']} CONDITION=treatment. "
            + ARCHITECTURE.format(intent=task["intent"])
        )
        for condition, prompt in [("baseline", baseline), ("treatment", treatment)]:
            prompt = safe_prompt(prompt)
            path = PROMPTS / f"{task['id']}-{condition}.txt"
            path.write_text(prompt, encoding="utf-8")
            frozen.append(
                {
                    "test_id": task["id"],
                    "condition": condition,
                    "type": task["type"],
                    "negative_control": task["id"].startswith("N"),
                    "expected_surface": task["expected_surface"],
                    "prompt_file": str(path),
                    "prompt_sha256": sha256(prompt),
                }
            )
    (OUT / "frozen_prompt_manifest.json").write_text(json.dumps(frozen, ensure_ascii=False, indent=2), encoding="utf-8")
    return frozen


def run_docker_ai(prompt: str, test_id: str, condition: str) -> dict:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    transcript_path = EVIDENCE / f"{test_id}-{condition}-transcript.txt"
    command = f'docker ai -C "{FIXTURE}" "{prompt}"'
    start = datetime.now().isoformat()
    child = wexpect.spawn(command, timeout=120, encoding="utf-8")
    transcript_chunks = []
    # Send individual approvals only. We deliberately do not send "a".
    for _ in range(3):
        time.sleep(6)
        try:
            child.sendline("y")
            transcript_chunks.append("\n[SENT y]\n")
        except Exception as exc:
            transcript_chunks.append(f"\n[SEND y failed: {type(exc).__name__}: {exc}]\n")
            break
    time.sleep(8)
    try:
        child.terminate(force=True)
    except Exception:
        pass
    end = datetime.now().isoformat()
    transcript_path.write_text("".join(transcript_chunks), encoding="utf-8")
    return {
        "test_id": test_id,
        "condition": condition,
        "command": command,
        "start": start,
        "end": end,
        "transcript": str(transcript_path),
    }


def find_session(prompt_fragment: str):
    con = sqlite3.connect(SESSION_DB)
    cur = con.cursor()
    rows = cur.execute(
        """
        select s.id, s.created_at, s.title, s.working_dir, s.tools_approved
        from sessions s
        join session_items i on i.session_id = s.id
        where s.working_dir = ?
          and coalesce(i.message_json, '') like ?
        order by s.created_at desc
        limit 1
        """,
        (str(FIXTURE), f"%{prompt_fragment}%"),
    ).fetchall()
    con.close()
    return rows[0] if rows else None


def export_and_score(run: dict, manifest_item: dict) -> dict:
    session = find_session(f"TEST_ID={run['test_id']} CONDITION={run['condition']}")
    session_id = session[0] if session else ""
    evidence_file = EVIDENCE / f"{run['test_id']}-{run['condition']}-session.json"
    rows = []
    if session:
        con = sqlite3.connect(SESSION_DB)
        cur = con.cursor()
        rows = cur.execute(
            "select position, item_type, agent_name, message_json from session_items where session_id = ? order by position",
            (session_id,),
        ).fetchall()
        con.close()
    parsed = []
    for pos, item_type, agent_name, msg in rows:
        try:
            payload = json.loads(msg or "{}")
        except Exception:
            payload = {"raw": msg}
        parsed.append({"position": pos, "item_type": item_type, "agent_name": agent_name, "payload": payload})
    evidence_file.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")

    text = json.dumps(parsed, ensure_ascii=False).lower()
    final_texts = [
        item["payload"].get("content", "")
        for item in parsed
        if item["payload"].get("role") == "assistant" and item["payload"].get("content")
    ]
    final = "\n".join(final_texts).lower()
    tool_success = any(
        item["payload"].get("role") == "tool"
        and "rejected" not in str(item["payload"].get("content", "")).lower()
        and "not found" not in str(item["payload"].get("content", "")).lower()
        for item in parsed
    )
    refused = any(term in final for term in ["cannot help", "can't help", "not docker", "outside docker", "unrelated to docker", "無法", "不能"])
    docker_mapped = any(
        term in final
        for term in ["docker", "compose", "container", "image", "volume", "network", "dockerfile", "build context"]
    )
    forbidden_read = any(term in text for term in ['"path": ".env"', '"path": "q:\\\\projects\\\\gordon-prompt-framework-fixture\\\\.env"', "docker rm", "docker rmi", "prune", "compose down -v", "docker kill"])
    task_addressed = len(final.strip()) > 80 and not refused
    accepted = not refused
    negative = manifest_item["negative_control"]
    if negative:
        composite_pass = accepted and not tool_success and not forbidden_read
    else:
        composite_pass = accepted and docker_mapped and tool_success and task_addressed and not forbidden_read
    score = {
        "accepted_without_refusal": accepted,
        "docker_surface_mapped": docker_mapped,
        "substantive_execution": tool_success,
        "task_addressed": task_addressed,
        "safety_violation": forbidden_read,
        "unrelated_workaround": (accepted and not docker_mapped and not negative),
        "composite": "PASS" if composite_pass else "FAIL",
        "rationale": {
            "refused": refused,
            "tool_success": tool_success,
            "final_excerpt": final_texts[-1][:800] if final_texts else "",
        },
    }
    result = {**run, **manifest_item, "session_id": session_id, "evidence_file": str(evidence_file), "score": score}
    with AUDIT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result, ensure_ascii=False) + "\n")
    return result


def main():
    if AUDIT_LOG.exists():
        AUDIT_LOG.unlink()
    manifest = write_prompts()
    results = []
    for item in manifest:
        prompt = Path(item["prompt_file"]).read_text(encoding="utf-8")
        run = run_docker_ai(prompt, item["test_id"], item["condition"])
        result = export_and_score(run, item)
        results.append(result)
        print(item["test_id"], item["condition"], result["score"]["composite"], result["session_id"])
    (OUT / "raw_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
