# Results Summary For Verification
Run ID: `gordon_prompt_arch_20260507_v1`
Fixture: `Q:\Projects\gordon-prompt-framework-fixture`
Primary evidence DB: `C:\Users\miles\.cagent\session.db`

## Positive Task Results
| Test | Type | Baseline | Baseline session | Treatment | Treatment session |
|---|---|---|---|---|---|
| `T01` | frontend/dev-server | PASS | `5183de0e-dad9-4fad-afe5-17af5e44d2dc` | PASS | `cc79801b-1e37-44f6-a8aa-e6a5fa110d49` |
| `T02` | backend/runtime | PASS | `6d8418ad-ed15-45dd-8dc9-f31fe6cf5847` | PASS | `3f6c586d-ebb0-4f60-9f69-70a4af0d8061` |
| `T03` | database/backend | PASS | `b1ebc8cd-7ac5-4c60-a0a7-02480b6dc362` | PASS | `b9cc135c-46d4-4f54-b031-40dc05c19e26` |
| `T04` | test/CI | PASS | `2819f074-d90c-403b-93ae-2f3992bf0bfa` | PASS | `0ce35aae-0157-45fc-942b-b12f70953144` |
| `T05` | image-optimization | PASS | `3f4f636a-ec9e-4e41-94d6-8b71008ed795` | PASS | `e6ea648a-a4d4-4658-8008-13c2b99ca480` |
| `T06` | logs/debugging | PASS | `324fb303-af9a-4f12-8a21-09e697c5175d` | PASS | `4c92cf33-9d80-4461-8eff-af12f4c7ef90` |
| `T07` | security/config | PASS | `0d424d23-5b72-4f31-bbc0-b578914964e9` | PASS | `74602a62-d29e-4990-853e-e3ff2ab70f60` |
| `T08` | documentation | PASS | `79876cdf-4923-4c45-a69f-c0fb37d8b80a` | PASS | `d77f992c-03ed-4fb4-9e73-2e95001aa6d5` |
| `T09` | architecture | PASS | `1fcd34be-8e41-4c76-9f8b-1f8c5ac21004` | PASS | `1c6163ab-cafd-4ad3-9f44-54f95e535d55` |
| `T10` | build-cache | PASS | `b645226f-50d3-459a-8f0a-949ac20aa4f5` | PASS | `40f3b2db-ecda-49b9-af7c-0c543d71912c` |
| `T11` | local-dev-parity | PASS | `b5acc874-a64d-4acd-bf0b-d352d250f5c9` | PASS | `184e5f8a-66ef-4867-a91d-cdc501d5cf1a` |
| `T12` | deployment-readiness | PASS | `3156fcc6-c418-4155-948b-8a94e9caadfb` | PASS | `8bd97419-7bf4-422f-873d-050886d42746` |

baseline positive pass rate: 12/12 = 100.0%

treatment positive pass rate: 12/12 = 100.0%

## Negative Controls
| Test | Condition | Auto score | Manual interpretation | Session |
|---|---|---|---|---|
| `N01` | baseline | PASS | PASS as general answer allowed; no Docker forcing required | `e87090eb-1fb5-40cf-b16a-582ed7d11d16` |
| `N01` | treatment | FAIL | PASS as negative control; Gordon refused artificial Docker mapping | `caeaa16e-a065-4d85-93dc-23df17d4fb00` |
| `N02` | baseline | FAIL | PASS as general answer allowed despite auto-score artifact | `f98ec4e1-d22b-4bac-a717-3faf99116df6` |
| `N02` | treatment | PASS | PASS as negative control; Gordon refused artificial Docker mapping before blind y artifact | `a8a84e53-d6c0-4522-ba86-3ee92f7f8981` |

## Caveats
- The runner blind-sent `y` individual approvals three times per run. Some sessions contain trailing `y` user messages after Gordon had already completed; scoring uses earlier tool/final evidence, but reports note this artifact.
- Treatment met the 80% target: 12/12 positive tasks passed.
- Baseline also passed 12/12 positive tasks, so the observed lift is 0 percentage points in this fixture.
- This means the prompt architecture is operationally acceptable for this corpus, but not proven to improve acceptance beyond Gordon baseline on Docker-adjacent fixture tasks.
