# Elsevier Article Retrieval access verified

Codex, 4 November 2026, Australia/Hobart.

Barry reported that Elsevier API Support had approved his use case and enabled
ScienceDirect Article Retrieval for his existing key, then authorised a test.
This supersedes the earlier repeated configuration-level HTTP 403 result.

Two requests retrieved DOI `10.1016/j.tree.2015.09.005`, López-García & Moreira
(2015), *Open Questions on the Origin of Eukaryotes*. Both used
`GET https://api.elsevier.com/content/article/doi/10.1016/j.tree.2015.09.005?view=FULL`,
`Accept: text/xml` and the existing key in `X-ELS-APIKey`. No key was placed in
the URL or printed. Redirects were disabled. No institutional token, browser
login or proxy configuration was added.

| Request origin | UTC time | HTTP | Bytes | XML structure |
|---|---|---|---|---|
| WSL laptop, GlobalProtect connection | 08:21:16 | 200 | 257,489 | Full-text retrieval response; one originalText and body, 11 section elements, 35 para elements |
| Campus server | 08:21:19 | 200 | 257,489 | Same structure |

Both responses report `openaccess=0` and have identical SHA256:
`fc6f6db1e910f5c787f9362cabe2d10c2b586f2c17cf53600eee78b9513de9bf`.
Neither contains a service-error element. Structural checks establish a body
payload beyond metadata; article completeness and scientific content were
not reviewed. The API key was read from its existing private credential file.
The laptop request used it transiently in memory without creating a local
credential file.

The campus response is retained in a restricted TDM probe directory, separate
from the canonical library. The laptop response was not saved. Only status,
structural counts and hashes entered the agent session; no article text did.
No library manifest or index was modified, and no bulk retrieval was started.
The dated probe script and two aggregate JSON receipts remain in ignored
`scratch/elsevier-probe-20261104/`.

**Observed conclusion:** the enabled key can retrieve this subscription article
from both origins. The current GlobalProtect route was accepted for this
request. This does not identify the university account or public egress address,
establish support for every VPN route, or establish entitlement to every article.

[Elsevier's API documentation](https://dev.elsevier.com/documentation/ArticleRetrievalAPI.wadl)
distinguishes API entitlement from content rights and supports XML full-text
retrieval. Its [authentication guidance](https://dev.elsevier.com/tecdoc_api_authentication.html)
describes institutional IP authentication and institutional tokens. These
documents explain the mechanism; the successful requests supply the evidence
for this particular connection.

Next owner: References Codex, for a bounded Elsevier library integration when
that work resumes. Keep subscription copies under the existing TDM custody
rules. The permission to retrieve does not settle the outstanding UTAS Library
question about sending licensed content to AI services.
