---
block: organization_metadata
---

Shows the details of an organization in an aside floated to the right of the text: its logo, contact person, contact email, contact phone number, country, organization size, website, and subjects.

The block stores none of these details. It reads them from an organization when it renders, so to change what it shows, change the organization. With no `organization_source`, that is the content item the block is on. A section without a value is left out, and if the source can't be read, the block shows nothing.

The block chooser offers this block only on `Organization` items.

### Fields

- `organization_source`: a list with at most one `{ "@id": path }` object, where `path` is the path or full URL of an `Organization` item. Leave it out to use the current item.

### Examples

A block that shows the organization it is on:

```json
{ "@type": "organization_metadata" }
```

A block that shows another organization:

```json
{
  "@type": "organization_metadata",
  "organization_source": [{ "@id": "/stakeholders/simples-consultoria" }]
}
```
