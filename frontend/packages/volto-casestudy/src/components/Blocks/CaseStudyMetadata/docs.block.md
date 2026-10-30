---
block: case_study_metadata
---

Shows the details of a case study in an aside: its preview image, organizations, providers, industry, usages, versions, website, and subjects.

The block stores none of these details. It reads them from a case study when it renders, so to change what it shows, change the case study. With no `case_study_source`, that is the content item the block is on. A section without a value is left out, and if the source can't be read, the block shows nothing.

The block chooser offers this block only on `CaseStudy` items.

### Fields

- `case_study_source`: a list with at most one `{ "@id": path }` object, where `path` is the path or full URL of a `CaseStudy` item. Leave it out to use the current item.
- `layout`: `full` spans the container, with the image first and the details below. `compact` is a narrow aside floated to the right of the text. Without a known value, the block uses `full`.

### Examples

A block that shows the case study it is on:

```json
{ "@type": "case_study_metadata" }
```

A compact block that shows another case study:

```json
{
  "@type": "case_study_metadata",
  "case_study_source": [{ "@id": "/case-studies/plone.org" }],
  "layout": "compact"
}
```
