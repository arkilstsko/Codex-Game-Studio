# Prepublish Checklist

## Legal and Attribution

- [ ] README credits the upstream project and links to its repository.
- [ ] NOTICE includes the upstream copyright and MIT license attribution.
- [ ] LICENSE is present.

## Install Verification

- [ ] `python3 codex-adapter/scripts/generate_codex_skills.py`
- [ ] `python3 scripts/validate_repo.py`
- [ ] `python3 codex-adapter/scripts/install_codex_skills.py --target /private/tmp/cgs-release-test --replace`
- [ ] Confirm `$ccgs-start`, `$ccgs-help`, `$ccgs-skill-test`, and `$ccgs-dev-story` appear after restarting Codex or starting a new thread.

## Runtime Checks

- [ ] Generated skills use relative `../ccgs-references/references` paths.
- [ ] `$ccgs-setup-engine` writes engine reference docs to the target project under `docs/engine-reference/`.
- [ ] Reference hooks are documented as manual/reference scripts, not automatic runtime hooks.
- [ ] `request_user_input` examples use Codex-supported single-choice schemas.

## GitHub Trust

- [ ] SECURITY.md points to private vulnerability reporting.
- [ ] Public issue templates warn users not to paste secrets or vulnerabilities.
- [ ] No placeholder clone URLs remain.
- [ ] CODEOWNERS/FUNDING are absent unless configured for the current owner.
