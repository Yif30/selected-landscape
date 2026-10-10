# Selected landscapes: data and code

Research data and analysis code for “Selected landscapes in short-video representations of urban places”.

The analytical unit is a scene within a research video record. Each research video record belongs to one sampled street block. The same platform video can appear in multiple block searches; research-video identifiers remain distinct throughout the analyses.

| Directory | Contents |
| --- | --- |
| [data/](data/README.md) | Video inventory, sampled blocks, scene table, environment table, behaviour table and linked scene records |
| [dictionaries/](dictionaries/README.md) | Manuscript categories, field definitions, element categories, behaviour subtype functions and transition states |
| [figure_data/](figure_data/README.md) | Direct numerical inputs for the quantitative panels of Figs. 1–3 |
| [results/](results/README.md) | Exposure ranking, model inputs, coefficients, contrasts and repeated-sampling estimates |
| [prompts/](prompts/README.md) | Manuscript-aligned video and downstream classification prompt templates |
| [code/](code/README.md) | Table preparation, descriptive estimators, role models, scene-element models and plotting |
| [config/](config/README.md) | Analysis seeds, repetition counts, exposure thresholds and sampling parameters |

## Data relationships

`blocks.block_id → videos.block_id → scenes.video_id`; environment and behaviour rows join to scenes through `scene_id`. Element identifiers join to `element_dictionary.csv`. `scenes.jsonl.gz` contains the corresponding linked scene representation. CSV files use UTF-8 with a byte-order mark.

All identifiers are strings. In particular, platform video identifiers exceed reliable spreadsheet numeric precision. Text import preserves leading zeros and complete platform identifiers.

`videos.csv` contains retrieval and archived research-video records. The field `in_retrieval_index` identifies records from the retrieval index; available platform identifiers provide canonical source links. `has_structured_scene` identifies research videos represented in the archived scene table; `classified_scene_count` counts released S1–S4 scenes. `has_archived_translation` records the presence of an archived translation associated with that research identifier. The reported collection month is recorded at month resolution. Blank source identifiers or links denote unavailable source-index metadata.

## Analytical definitions

Scene forms are S1 Local scenes, S2 Curated local scenes, S3 Glocal scenes and S4 Global scenes. Environmental categories follow the seven definitions in the classification codebook. Released environmental associations use the final element dictionary. Human-only labels, mobile personal objects and labels lacking a physical environmental assignment are outside this environmental vocabulary. Behaviour subtypes determine the two functional classes through the released crosswalk; the six broad behaviour classes alone do not determine function.

Scene and environmental exposure estimates use scene-duration weights. Repeated mentions of the same element within a scene contribute one association. Behaviour counts use role–behaviour records. Behaviour-duration composition weights each role–behaviour record by its scene duration. Provincial behaviour TVD uses the six behaviour classes pooled across roles. Focal-media node values are equal-weight means of block-level duration shares within each province. Role regression observations are distinct scene–role–function combinations; category shares use the number of distinct released elements in the scene, with zeros for scenes lacking environmental elements.

Role models are separate unweighted logistic models for focal and background figures, with covariance clustered by research-video identifier. Environmental models enter one category share at a time and adjust for scene form and log(1 + duration). Probability changes are local average marginal effects scaled to a 10-percentage-point category-share increment. Scene-only models adjust for duration; marginal probabilities average over the observed role-specific duration distribution.

Transitions connect consecutive observations of each role within the research video. Scenes without that role can be skipped. Each set-to-set transition contributes total mass one across the eight functional states; weights are aggregated to six broad behaviour classes before row normalisation. Individuals are not tracked.

Scene-element prediction uses binary element presence, balanced sampling of S1–S4 within each eligible block and a maximum of 50 scenes per form per block. Train/test assignment occurs at block level. The nested exposure-ranked vocabularies and all 100 repetitions are calculated by the released scripts. Rarefaction uses all classified S1–S4 scenes, including scenes with no released environmental elements, and the same released element vocabulary. Blocks require at least 20 scenes of each form; the supplied design includes 187 blocks and 17,391 unordered block pairs, five sample depths and 50 repetitions. Empty-union Jaccard pairs contribute zero. Empirical intervals are 2.5th–97.5th percentiles.

All numerical figure inputs are calculated from the released tables. Plotting creates quantitative panels from these inputs. Video illustrations and boundary geometry are separate from the numerical panel inputs.

## Execution

Python 3.10 was used for the supplied calculations. From the package directory:

```bash
python -m pip install -r requirements.txt
python code/run_all.py
```

Plots alone, using the supplied direct figure data:

```bash
python code/run_all.py --figures-only
```

A custom plot destination can be set with `--output PATH`. Full calculations generate CSV outputs in `results/` and `figure_data/`; plots are generated in `figures/`. Statistical calculations run locally and do not require model-service credentials.

## Citation and licences

Citation metadata are in `CITATION.cff`. Data, dictionaries, prompts and numerical outputs are provided under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Analysis code is provided under the [MIT licence](https://opensource.org/license/mit). These licences apply to the research contributions in this package. Source videos retain their respective rights.

P1–P5 are revised prompt templates aligned with the final manuscript taxonomy: four scene forms, seven environmental categories, six behaviour classes and two functional classes. Template fields and examples follow the released classification dictionaries. The full subtype-function crosswalk is included in P5. Numerical analyses read the released structured tables.

## Folder documentation and package files

Every directory contains a README describing its files, formats, relationships and field meanings. Figure-specific fields are documented in [Fig1](figure_data/Fig1/README.md), [Fig2](figure_data/Fig2/README.md) and [Fig3](figure_data/Fig3/README.md). Data identifiers, units and missing values are documented in [data/README.md](data/README.md); model and repeated-sampling fields are documented in [results/README.md](results/README.md). Folder guides include Chinese field explanations.

| File | Purpose and form |
| --- | --- |
| [README.md](README.md) | English package overview, analytical definitions and execution commands; Markdown |
| [README_zh.md](README_zh.md) | Chinese package overview and navigation; Markdown |
| [requirements.txt](requirements.txt) | Python package names and exact dependency versions, one package==version per line |
| [CITATION.cff](CITATION.cff) | Citation metadata in CFF/YAML: cff-version, message, title, type, version, authors and license; author records use family-names and given-names |
| [LICENSE_DATA.md](LICENSE_DATA.md) | Licence scope and attribution for data, dictionaries, prompts and numerical outputs; Markdown |
| [LICENSE_CODE.txt](LICENSE_CODE.txt) | MIT licence for analysis code; plain text |
| [.gitignore](.gitignore) | Git exclusion patterns for Python cache files and generated figures; plain text |
