const { algoliasearch, instantsearch } = window;

const searchClient = algoliasearch('FBCOWM9UO9', 'fe585fa7c5e384b3bc76abe3aa6c74e7');

const search = instantsearch({
  indexName: 'ander1716_github_io_fbcowm9uo9_pages',
  searchClient,
  future: { preserveSharedStateOnUnmount: true },
  
});


search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),
  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
      item: (hit, { html, components }) => html`
<article>
  <img src=${ hit.path } alt=${ hit.title } />
  <div>
    <h1>${components.Highlight({hit, attribute: "title"})}</h1>
    <p>${components.Highlight({hit, attribute: "description"})}</p>
    <p>${components.Highlight({hit, attribute: "url"})}</p>
  </div>
</article>
`,
    },
  }),
  instantsearch.widgets.configure({
    hitsPerPage: 8,
  }),
  instantsearch.widgets.pagination({
    container: '#pagination',
  }),
]);

search.start();

