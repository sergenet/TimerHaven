# iOS release checklist

The iOS app is the Expo project in this repository (bundle id `com.sergenet.TimerHavenApp`,
App Store id `6756510490`). It ships through EAS. Ship a build in this order — each step
produces what the next one needs.

Copy for the store lives in [store.config.json](store.config.json), which is generated from
[tools/write_store_listings.py](tools/write_store_listings.py). Never hand-edit
`store.config.json`: the next generator run overwrites it, exactly like the Play metadata in
the Android repo.

## 1. Start from a clean, current `main`

- [ ] `git status` is clean and `git pull` brings nothing new
- [ ] `python tools/check_store_listings.py` exits `0`, meaning all seven storefronts still
      show the copy in this repo — or the drift is copy you are about to publish in step 3

## 2. Bump the version and regenerate the copy

- [ ] `python tools/prepare_release.py --version-name X.Y.Z`
      It bumps `expo.version` in [app.json](app.json) and `version` in [package.json](package.json),
      regenerates the listings, and runs the drift check. `--dry-run` shows the bump and writes
      nothing.
- [ ] Changing listing copy? Edit [tools/write_store_listings.py](tools/write_store_listings.py)
      before running it, and commit the regenerated `store.config.json` with the bump
- [ ] The build number is not bumped here on purpose: [eas.json](eas.json) sets
      `appVersionSource: remote` with `autoIncrement: true`, so EAS assigns the build number it
      will accept. A local bump would only disagree with the store.

## 3. Publish the listing copy (only when it changed)

- [ ] `python tools/prepare_release.py --publish` — it re-runs the comparison, asks before
      pushing, runs `eas metadata:push --non-interactive`, and only then re-checks. Add `--yes`
      for an unattended run; with no drift it publishes nothing.
- [ ] It must end with `published and verified: the App Store now serves the regenerated listings`.
      A push that cannot be confirmed fails the step instead of claiming success.
- [ ] No ASC credentials on the machine? Edit the copy in App Store Connect by hand and re-run
      `python tools/check_store_listings.py` until it exits `0`.

## 4. Build and submit

- [ ] `eas build -p ios --profile production` — EAS builds on a macOS image and assigns the build number
- [ ] `eas submit -p ios --profile production` — uploads the build to App Store Connect
- [ ] Install the TestFlight build and check the app still opens, the 15 tools load from the
      bundled payload, and the weather location prompt works

## 5. Review and release

- [ ] App Store Connect: add release notes for the version, then submit for review
- [ ] Choose manual or automatic release; on manual release, release once approved

## 6. Afterwards

- [ ] `python tools/check_store_listings.py` exits `0` for the newly released version
- [ ] The next 06:37 UTC drift run is green
- [ ] The version on the App Store product page matches [app.json](app.json) on `main`

## What the drift check verifies

| Field | Checked against the live store? | How |
|---|---|---|
| Title | yes | public App Store lookup API, per storefront |
| Description | yes, line by line | same API |
| Served language | yes | the storefront's reported localization |
| Subtitle | **no** | Apple exposes no public API for it |
| Keywords | **no** | Apple exposes no public API for them |

The report names subtitle and keywords as unverified rather than counting them as a match, so
the gap is visible. Everything else is a real comparison against what customers see.

## How the daily check behaves

[.github/workflows/store-listings-drift.yml](.github/workflows/store-listings-drift.yml) runs at
06:37 UTC, on demand, and on every pull request into `main`.

- Daily and manual runs **fail** on drift and open one issue titled *Store listing drift
  detected*; later runs comment on that issue instead of filing another, and the first run that
  matches closes it
- Pull requests only **report** drift, so a PR that edits listing copy is not blocked from merging
- It needs no repository secret: Apple's lookup API is public, and the workflow never writes to
  the store

## Credentials

Nothing in this repo holds a credential.

- The drift check needs none.
- Publishing copy and uploading builds authenticate through your Expo login (`eas login`) plus
  the App Store Connect credentials EAS already holds for this project — run `eas credentials -p ios`
  to inspect them. Keep them with EAS, never in a file here.
- If you later add a CI job that publishes, put the key in GitHub *Settings → Secrets and
  variables → Actions* as a repository secret, and read it through `secrets.*`; do not commit it.

## If something goes wrong

- [ ] Pausing a release: App Store Connect → the version → *Pause rollout* for a phased release
- [ ] A bad build cannot be replaced in place; fix forward with a new build number (EAS does this)
- [ ] Published copy can be corrected the same way, and the drift check lists exactly which lines
      disagree before you republish
- [ ] If `prepare_release.py` says `npx is not installed`, install EAS CLI (`npm i -g eas-cli`)
      or run the publish step from a machine that has it
