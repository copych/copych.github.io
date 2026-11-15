[Main Page](https://copych.github.io/)

## Metronome branch installer

[Install feature-metronome-training-games](https://copych.github.io/feature-metronome-training-games/webapp/installer/)

This repository publishes prepared, verified installer sites. The firmware is
built in `copych/FM1-Ear-Trainer` by its required shared attested workflow.
The source repository's `verify` job checks checksums, attestations, signer,
source revision and recovery/resource pairing before uploading `verified-site`.
The contents of that artifact are placed under their source branch name here.

The earlier "Deploy all branches" workflow exported this hosting repository's
own branches. It could not build a different repository's firmware or create
the generated installer files. The workflow now validates the prepared branch
sites and publishes them, preserving their package hashes and source manifests.

To update: use a successful branch build's `verified-site` artifact, check its
source revision and branch, replace that branch's prepared directory, and
commit it. `tools/assemble-pages.py` rejects local/unattested builds, missing
recovery/editor files and package/resource/WASM hash mismatches. Source and
build links remain in each site's installer and `build-info.json`.
