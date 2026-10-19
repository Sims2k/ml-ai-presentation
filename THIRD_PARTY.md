# Third-party material

## Requested temporal-drift figure

`assets/references/drift-types-krawczyk-cano.jpg` reproduces Figure 2 from:
Bartosz Krawczyk and Alberto Cano, *Online Ensemble Learning with Abstaining
Classifiers for Drifting and Noisy Data Streams*, Applied Soft Computing 68,
677–692 (2018).

- Presenter-supplied figure: https://www.researchgate.net/figure/Four-types-of-concept-drift-according-to-severity-and-speed-of-changes-and-noisy-blips_fig2_321627304
- Original image link: https://www.researchgate.net/profile/Alberto-Cano-2/publication/321627304/figure/fig2/AS:591947903303681@1518142786882/Four-types-of-concept-drift-according-to-severity-and-speed-of-changes-and-noisy-blips_W640.jpg
- Identical figure retrieved intact from page 6 of this public lecture PDF:
  https://pyconf.hydpy.org/PyConf19Slides/talks/The-Past-and-the-dubious-Concept-Drift.pdf
- Publication listing: https://canoalberto.github.io/

Direct image retrieval returned HTTP 403, so the publicly posted copy was used.
The graphic's shapes and labels are unmodified. The slide's explanatory text and
bank examples are new. The original authors/publisher retain rights; this asset
is not claimed as original code or covered by a repository-wide open-source license.

## Tool logos and interface icons

Small marks identify tools discussed in the lecture; they do not imply endorsement.
The original SVG files and their upstream URLs are stored in `assets/marks/`.

- Apache Airflow logo: official community branding resources,
  https://airflow.apache.org/community/resources/ ; downloaded from
  https://airflow.apache.org/images/airflow-logo-small.svg . Apache Airflow and
  its logo are trademarks of the Apache Software Foundation.
- MLflow logo: official project asset,
  https://github.com/mlflow/mlflow/blob/master/assets/logo.svg . MLflow retains
  its applicable trademark rights. The mark is embedded without recoloring.
- Concept and component icons: Lucide, https://lucide.dev/ , obtained from the upstream
  `lucide-icons/lucide` repository. The SVGs are used in the lecture accent
  color; the ISC license and the included Feather-derived notices are preserved
  in `licenses/Lucide-LICENSE.txt`.

Icons identify data stores, models, training, policy, checks, recovery, customer
cohorts and other responsibilities throughout the lecture. Component pictograms
use Lucide SVG primitives inside the authored diagrams; header marks remain
embedded SVG images.

Logos and icons are embedded in the HTML as local SVG data, so viewing the
presentation does not depend on a third-party image CDN.

## Fonts

Cormorant Garamond, Source Sans 3, and IBM Plex Mono are embedded for offline
viewing. Their upstream license texts are in `licenses/`. No claim is made to
ownership of the font software.

## Presentation tooling

The presentation applies Frontend Slides' fixed-stage layout and Diagram Design's
SVG/motion approach. Generated figure geometry, lecture content, and build code
are included so colleagues can edit them. No local skill-installation instructions,
credentials, connector configuration, or agent-session data is included.
