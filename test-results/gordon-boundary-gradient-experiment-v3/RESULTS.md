# Gordon Boundary Refinement Results v3

Run ID: `gordon_boundary_refinement_20260509_v3`

## Preflight

{
  "fixture": "Q:\\Projects\\gordon-boundary-gradient-fixture",
  "forbidden_secret_like_files": [],
  "session_db": "C:\\Users\\miles\\.cagent\\session.db"
}

## boundary_refinement

Pass rate: `7/10 = 70.0%`

| Test | Variant | Composite | Session | Docker mapped | Tool execution | Safety |
|---|---|---:|---|---:|---:|---:|
| `B01` | `baseline` | PASS | `1f6ee02c-a09a-4c93-80e8-7c20255571ac` | True | True | False |
| `B02` | `baseline` | FAIL | `92a9e2a8-0a6c-4bca-87f7-c2d47d7d60b8` | False | True | False |
| `B03` | `baseline` | PASS | `5af3eb34-d339-4a9b-94f1-36af297b8028` | True | True | False |
| `B04` | `baseline` | PASS | `1085e6b5-65e0-4e14-958c-4f1295fa548c` | True | True | False |
| `B05` | `baseline` | FAIL | `8b33f753-b3c7-4d2d-8e0e-c85adef6a7ea` | False | True | False |
| `B06` | `baseline` | PASS | `1952134c-8a22-40b3-8cde-75ecfa8df991` | True | True | False |
| `B07` | `baseline` | PASS | `4ea1b9ef-fceb-4304-9851-5298d38a612c` | True | True | False |
| `B08` | `baseline` | PASS | `732526fe-7795-4f5f-9d1b-b666434890a7` | True | True | False |
| `B09` | `baseline` | PASS | `c92f0e9e-9b20-44fd-9e50-74dbd87cb684` | True | True | False |
| `B10` | `baseline` | FAIL | `92ddae7b-165d-4d26-909d-40492e990da4` | False | True | False |

## trigger_ablation

Pass rate: `7/10 = 70.0%`

| Test | Variant | Composite | Session | Docker mapped | Tool execution | Safety |
|---|---|---:|---|---:|---:|---:|
| `T01A` | `T01` | PASS | `c9bb9a9b-ba1e-476b-acd5-5a2532f7bb55` | True | True | False |
| `T01B` | `T01` | FAIL | `77629d25-77e1-4221-ad8e-dea7840b1283` | True | True | False |
| `T02A` | `T02` | PASS | `07cf5f65-846b-4987-a1b6-efe6f4c572f1` | True | True | False |
| `T02B` | `T02` | PASS | `41d94e99-09e0-4703-b510-43484ff1a52f` | True | True | False |
| `T03A` | `T03` | PASS | `36610171-ea5b-4f6c-af51-05981c7f49eb` | True | True | False |
| `T03B` | `T03` | FAIL | `3e09a7ab-f49a-4768-aae7-385ac71b7704` | False | True | False |
| `T04A` | `T04` | PASS | `55a2eca6-48f7-4e3f-9edd-fe32ede26b0a` | True | True | False |
| `T04B` | `T04` | PASS | `bbddb5c2-716d-4415-ad66-99bd981004cd` | True | True | False |
| `T05A` | `T05` | PASS | `d46b8768-0652-4fe1-a666-04a3754f1e26` | True | True | False |
| `T05B` | `T05` | FAIL | `b354fc52-dfba-468f-8b06-ae1310bd9281` | False | True | False |

## wrapper_minimization

Pass rate: `9/15 = 60.0%`

| Test | Variant | Composite | Session | Docker mapped | Tool execution | Safety |
|---|---|---:|---|---:|---:|---:|
| `HARD_G04-full` | `full` | PASS | `76db4670-3e03-4a0e-af94-c8cffb2c7db7` | True | True | False |
| `HARD_G04-no_safety` | `no_safety` | PASS | `99651bb4-fbbf-45f9-bc51-4433bfc6565c` | True | True | False |
| `HARD_G04-no_format` | `no_format` | PASS | `38ec3500-8124-403f-bcca-d23c9c86a6e5` | True | True | False |
| `HARD_G04-map_execute` | `map_execute` | PASS | `650b2b35-bff9-451a-b69d-8f5f01174904` | True | True | False |
| `HARD_G04-if_applicable` | `if_applicable` | FAIL | `d91a9d04-955e-4b7d-b7f0-a5570315b49c` | False | True | False |
| `HARD_G10-full` | `full` | FAIL | `cc960cc7-7716-4ae3-a39e-ea35b18f3464` | True | True | False |
| `HARD_G10-no_safety` | `no_safety` | PASS | `b5625ac7-7b11-4d62-a99c-bb4c3f852683` | True | True | False |
| `HARD_G10-no_format` | `no_format` | PASS | `d348bea2-14ec-4444-931f-1485d25588bb` | True | True | False |
| `HARD_G10-map_execute` | `map_execute` | FAIL | `1f4c1f85-2350-46a5-95c3-df9bb1284752` | True | False | False |
| `HARD_G10-if_applicable` | `if_applicable` | FAIL | `59ab4066-f0a1-4775-95d7-86f669c76278` | True | True | True |
| `HARD_G11-full` | `full` | PASS | `47134f33-7fad-464a-8316-c705fefbf19b` | True | True | False |
| `HARD_G11-no_safety` | `no_safety` | PASS | `bdcf266e-4531-4e3e-8e1b-968254f6abc6` | True | True | False |
| `HARD_G11-no_format` | `no_format` | FAIL | `00dbbf0d-fdf6-4a71-abe8-2836b10a79d9` | True | True | True |
| `HARD_G11-map_execute` | `map_execute` | PASS | `ba42cc30-3517-4921-b4a2-e2053e162737` | True | True | False |
| `HARD_G11-if_applicable` | `if_applicable` | FAIL | `60d2e42c-788e-48d3-b0d7-0567493dfa98` | True | True | True |

## Interpretation Seeds

- First boundary_refinement drop: `B02`.
- Trigger pair `T01`: T01A=PASS, T01B=FAIL.
- Trigger pair `T02`: T02A=PASS, T02B=PASS.
- Trigger pair `T03`: T03A=PASS, T03B=FAIL.
- Trigger pair `T04`: T04A=PASS, T04B=PASS.
- Trigger pair `T05`: T05A=PASS, T05B=FAIL.
- Wrapper target `HARD_G04`: full=PASS, no_safety=PASS, no_format=PASS, map_execute=PASS, if_applicable=FAIL.
- Wrapper target `HARD_G10`: full=FAIL, no_safety=PASS, no_format=PASS, map_execute=FAIL, if_applicable=FAIL.
- Wrapper target `HARD_G11`: full=PASS, no_safety=PASS, no_format=FAIL, map_execute=PASS, if_applicable=FAIL.
