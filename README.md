# GitHub Actions CI/CD Demo

A small Python calculator project that demonstrates continuous integration and
continuous delivery with GitHub Actions. CI tests and packages every pull
request and push to `main`. CD publishes a Docker image to GitHub Container
Registry (GHCR) only after CI succeeds for a push to `main`.

> CD in this demo means **continuous delivery of a versioned container image**.
> It does not deploy to a running server or cloud account; no deployment target
> was specified.

## Project layout

```text
.
├── .github/workflows/
│   ├── ci.yml             # Test, build, Docker validation, artifact upload
│   └── cd.yml             # Publish the tested image to GHCR
├── app/                   # Calculator application
├── tests/                 # Automated tests
├── Dockerfile
├── build.sh               # Creates the downloadable application bundle
└── requirements.txt
```

## CI vs CD

- **Continuous Integration (CI)** frequently integrates changes and checks
  them automatically. Here, a push or pull request runs tests, packages the
  application, verifies the Docker image builds, and saves a downloadable
  artifact.
- **Continuous Delivery (CD)** takes a change that passed CI and prepares a
  deployable release. Here, a successful push to `main` publishes the Docker
  image to GHCR. Pull requests and failed CI runs cannot publish.
- **Continuous deployment** would additionally roll that release out to a live
  environment automatically. That is intentionally outside this demo.

## GitHub Actions concepts in this project

- A **workflow** is a YAML automation in `.github/workflows/`; these are the
  separate CI and CD pipelines.
- **Events** (`push`, `pull_request`, `workflow_run`) decide when a workflow
  starts. `workflow_dispatch` also permits manually starting CI.
- **Jobs** are units of work executed on a **runner**. The CI `build` job has
  `needs: test`, so it cannot run unless tests pass. CD runs on a GitHub-hosted
  `ubuntu-latest` runner after the successful CI workflow.
- **Steps** are individual commands or reusable actions within a job, such as
  checking out code, setting up Python, running pytest, and uploading an
  artifact.
- **Secrets** are sensitive values made available to a workflow without
  hard-coding them. CD uses GitHub's automatically provided
  `secrets.GITHUB_TOKEN` to authenticate to GHCR. Its permissions are limited
  to `contents: read` and `packages: write`; no personal access token or
  manually configured secret is needed.
- **Artifacts** are files produced by a workflow. CI uploads the contents of
  `build/` under a commit-specific artifact name; find it on the successful
  CI run's **Artifacts** section. The container image is the CD deliverable.

## Run locally

Requires Python 3.12 or newer and pytest.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
bash build.sh
python -m app.calculator
```

Try `10 + 5`, `-2 * 3`, or `10 / 0`; type `q` to exit. The last expression
prints a user-friendly division-by-zero error.

## Build and run the Docker image

Install and start Docker Desktop first, then from the project root:

```bash
docker build -t calculator-demo:local .
docker run --rm -it calculator-demo:local
```

## Run the pipelines on GitHub

1. Create an **empty** GitHub repository (do not initialize it with a README,
   license, or `.gitignore`).
2. In this project folder, run the commands below, replacing the URL with the
   HTTPS URL of your repository:

   ```bash
   git init
   git add .
   git commit -m "Build GitHub Actions CI/CD demo"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git push -u origin main
   ```

3. On GitHub, open **Actions**. The push starts **CI Pipeline**. Open its run
   and verify **Test application** and **Build and package** pass. The build
   job uploads the `calculator-build-<commit>` artifact.
4. After CI succeeds, **CD Pipeline** starts automatically. Confirm its
   publish job succeeds, then open the repository's **Packages** page to find
   the `latest` and `sha-<commit>` container tags.
5. If package publishing is denied, open the repository's **Settings →
   Actions → General** and enable **Read and write permissions** for
   `GITHUB_TOKEN`. The workflow also declares the required job-level
   `packages: write` permission.

To download and run the published image (replace the owner/repository):

```bash
docker pull ghcr.io/YOUR_USERNAME/YOUR_REPOSITORY:latest
docker run --rm -it ghcr.io/YOUR_USERNAME/YOUR_REPOSITORY:latest
```

## Capture successful-run screenshots

The Actions screenshots need to come from the actual runs in your GitHub
repository; they cannot be generated before you push and GitHub executes the
workflows. After both runs succeed:

1. Capture the CI run page showing the completed green jobs and uploaded
   artifact.
2. Capture the CD run page showing the successful publish job (and, if useful,
   the repository Packages page with the published tags).
3. Save the images in `docs/screenshots/` as `ci-success.png` and
   `cd-success.png`, then commit and push them:

   ```bash
   mkdir -p docs/screenshots
   # Save your screenshots as docs/screenshots/ci-success.png and cd-success.png
   git add docs/screenshots
   git commit -m "Add successful pipeline screenshots"
   git push
   ```

Do not add credentials, `.env` files, access tokens, or private keys to
screenshots or the repository.

## See a failed CI run (optional)

Change an expected value in a test, push the change, and observe that the test
job fails and the build job is skipped. Restore the test, push again, and
confirm CI passes. CD does not publish an image for the failed run.
