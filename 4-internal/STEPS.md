# docs/ — Access & Encryption Guide

Files matching `*interna*` in this folder are encrypted with **git-crypt**.
They appear as binary garbage to anyone without access. Only authorized GPG key holders can decrypt them.

---

## One-time setup (authorized users)

### 1. Generate a GPG key (skip if you already have one)

```bash
gpg --full-generate-key
# Choose: RSA and RSA, 4096 bits, no expiry
# Use your real work email
```

### 2. Export your public key and send it to Diego

```bash
gpg --export --armor your@email.com > yourname-pubkey.asc
# Send yourname-pubkey.asc to Diego via secure channel (not email attachment to repo)
```

### 3. After Diego grants you access and pushes

```bash
git pull
git-crypt unlock   # uses your local GPG private key automatically
```

The `*interna*` files will be transparently decrypted from that point forward.

### 4. If cloning for the first time (instead of pulling)

```bash
git clone git@github.com:diegotrujillo-jikko/reto-ai-first-fase1.git
cd reto-ai-first-fase1
git-crypt unlock
```

Install git-crypt first if needed: `brew install git-crypt`

---

## Granting access to a new person (repo owner only)

```bash
# Import their public key
gpg --import yourname-pubkey.asc

# Add them to git-crypt
git-crypt add-gpg-user their@email.com

# Commit and push — a new encrypted key blob is added under .git-crypt/
git add .git-crypt/
git commit -m "chore: grant git-crypt access to <name>"
git push
```

---

## Revoking access

git-crypt has no built-in revoke. Steps:

1. Remove the person's key blob from `.git-crypt/keys/default/0/`
2. Rotate the symmetric key: `git-crypt init` on a fresh repo (rare, nuclear option)
3. Consider rotating secrets if the repo contains any

---

## Encrypted files in this repo

| Pattern | Why |
|---------|-----|
| `4-internal/*interna*` | Internal evaluation docs — not for participants |
| `4-internal/input_*` | Internal input files — not for participants |
