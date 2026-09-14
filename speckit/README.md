# Spec Kit integrations

This molecule provisions the pinned official `specify-cli` and declares the
agent integrations it supports. It deliberately does not copy Spec Kit skill
files into the molecule: the official CLI owns each agent's file layout and
integration semantics.

The molecule is version `1.1.0` and pins `specify-cli==1.0.6`. The declaration
covers the integration keys reported by `specify-cli 1.0.6`, including Claude
Code, Codex CLI, Gemini CLI, and the other supported agent/IDE integrations.

## Adoption

Adopt and install the molecule in one invocation:

```bash
spaex add https://github.com/haexmas/atoms \
  com.github.haexmas.atoms.speckit \
  --speckit-agents all
```

For a smaller selection, use a comma-separated list such as
`--speckit-agents claude,codex`. The selection is persisted in the project's
spaex install lock, so later installs do not prompt or reinstall unchanged
integrations.

The molecule enables the official CLI's explicit multi-install `--force` flag
because the declared set includes integrations that the CLI does not mark as
multi-install safe. This does not enable global installation.

The generic integration is configured with `--commands-dir .specify/commands`,
matching the project's Spec Kit command directory.

The molecule installs project-local integrations only. It never requests a
global agent installation and never embeds mutable or agent-specific skill
content.
