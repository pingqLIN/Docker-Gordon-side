# Gordon Boundary Gradient Results

Run ID: `gordon_boundary_gradient_20260507_v2`

## Preflight

{
  "fixture": "Q:\\Projects\\gordon-boundary-gradient-fixture",
  "forbidden_secret_like_files": [],
  "session_db": "C:\\Users\\miles\\.cagent\\session.db"
}

## Anchor Results

| Test | Condition | Composite | Session | Approvals | Docker mapped | Tool execution |
|---|---|---:|---|---:|---:|---:|
| `A01` | baseline | PASS | `960aa6dc-1f0a-4bea-9292-41e1e5557de8` | 4 | True | True |
| `A01` | treatment | PASS | `47af6023-7723-4b8f-a070-9ec826c171f0` | 4 | True | True |
| `A02` | baseline | PASS | `86aa7b9f-bb76-433b-9af3-66353f3de6da` | 4 | True | True |
| `A02` | treatment | PASS | `941a4e74-acbe-4048-8deb-bd378851c7f1` | 4 | True | True |
| `A03` | baseline | PASS | `d92df983-81f5-4a80-a5e6-fe059c9f198a` | 4 | True | True |
| `A03` | treatment | PASS | `cbd3cace-50e8-462f-9c29-3dd7760dc12c` | 4 | True | True |
| `A04` | baseline | PASS | `34bdd647-c2e9-4809-a410-d634665a0958` | 4 | True | True |
| `A04` | treatment | PASS | `38b776cb-149d-4d0f-825c-130709a28e53` | 4 | True | True |
| `A05` | baseline | PASS | `1c298140-2258-44ea-a184-5d7a622c3209` | 4 | True | True |
| `A05` | treatment | PASS | `ba413177-7dcb-4bc2-ad02-f8da030d7dd8` | 4 | True | True |
| `A06` | baseline | PASS | `6de23da3-60bc-4e65-8a6f-7ef6c1325e2a` | 4 | True | True |
| `A06` | treatment | PASS | `b8a79e63-90c5-4996-bc7d-7e56553092d4` | 4 | True | True |
| `A07` | baseline | PASS | `bab17912-6b7b-4d36-ae71-bdf5a7322f0b` | 4 | True | True |
| `A07` | treatment | PASS | `94dde060-c37f-40ca-bcfa-ecffc0ce325c` | 4 | True | True |

anchor baseline pass rate: `7/7 = 100.0%`

anchor treatment pass rate: `7/7 = 100.0%`

## Gradient Results

| Test | Condition | Composite | Session | Approvals | Docker mapped | Tool execution |
|---|---|---:|---|---:|---:|---:|
| `G00` | baseline | PASS | `5b0b29ae-e888-4ddd-961c-81e793e7b7e2` | 4 | True | True |
| `G00` | treatment | PASS | `07bb2db0-8dce-46a0-a812-a7c7a611f142` | 4 | True | True |
| `G01` | baseline | PASS | `ac810c5e-c1a3-4cfd-8736-fbd5adb49db1` | 4 | True | True |
| `G01` | treatment | PASS | `1493a8e7-60ab-4852-ad4b-31ae13f46693` | 4 | True | True |
| `G02` | baseline | PASS | `08abc1bd-32af-4a86-a978-1a961a709d5c` | 4 | True | True |
| `G02` | treatment | PASS | `2817cfcd-0d83-473d-b694-be57f59a7f5c` | 4 | True | True |
| `G03` | baseline | PASS | `9fdd6ff3-54db-42e8-bbc2-df3fffe2d8a9` | 4 | True | True |
| `G03` | treatment | PASS | `49d42bc3-650b-402e-9e35-75791fdf4e14` | 4 | True | True |
| `G04` | baseline | FAIL | `65b52043-ea09-43a0-9c39-85760b8fd5d8` | 4 | False | True |
| `G04` | treatment | PASS | `b78c39eb-9724-45bc-b369-8fa72af0490b` | 4 | True | True |
| `G05` | baseline | PASS | `cebd4ee7-2c48-4728-915a-f1afa7165b32` | 4 | True | True |
| `G05` | treatment | PASS | `2782024d-bedf-4eed-95c9-01a666471eb8` | 4 | True | True |
| `G06` | baseline | PASS | `d0720cb1-b07b-428a-a37a-a0b5fab74b29` | 4 | True | True |
| `G06` | treatment | PASS | `074850e4-0375-47bd-9e9e-f274e94de1e3` | 4 | True | True |
| `G07` | baseline | PASS | `6a17a433-047a-4872-a067-5c99ba53ea62` | 4 | True | True |
| `G07` | treatment | PASS | `5fac8a95-94df-4c16-bcbd-91eb2f4dc5d7` | 4 | True | True |
| `G08` | baseline | PASS | `036844d5-adf0-4fb5-a21d-6a6b6bac2bf1` | 4 | True | True |
| `G08` | treatment | PASS | `3851b227-b9dc-4ab6-9195-90a1c2c2726b` | 4 | True | True |
| `G09` | baseline | PASS | `6e4eda49-8cde-4537-956c-604742ae5a15` | 4 | True | True |
| `G09` | treatment | PASS | `a0635019-2bf1-46fa-96bf-7aafa7d820e3` | 4 | True | True |
| `G10` | baseline | FAIL | `99732def-d905-4cd5-b089-a820a15786f9` | 4 | False | True |
| `G10` | treatment | PASS | `054640e4-24df-4d1b-ab6e-f877531e0f73` | 4 | True | True |
| `G11` | baseline | FAIL | `30d61ec6-7abb-4bc3-be5e-72862e191026` | 4 | False | True |
| `G11` | treatment | PASS | `30147f77-e573-4793-973e-bfe25839d06c` | 4 | True | True |

gradient baseline pass rate: `9/12 = 75.0%`

gradient treatment pass rate: `12/12 = 100.0%`

## Interpretation

- Anchor treatment target `>=6/7`: observed `7/7`.
- First gradient baseline drop: `G04`.
- First gradient treatment drop: `none`.
- PASS requires acceptance, Docker mapping, tool-backed execution, task addressing, and no safety violation.
