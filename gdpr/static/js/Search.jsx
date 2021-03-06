import React, { Component } from "react";
import ReactDOM from "react-dom";

import {
  InstantSearch,
  SearchBox,
  Index,
  Configure
} from "react-instantsearch/dom";
import key from "keyboard-shortcut";

import ConnectedChapters from "./Chapters";
import ConnectedArticles from "./Articles";
import ConnectedRecitals from "./Recitals";
import ConnectedSections from "./Sections";
import ConnectedPagination from "./Pagination";

class Search extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  componentWillMount() {
    key("escape", this.onEscape);
  }

  onEscape() {
    document.body.classList.toggle("searching", false);
  }

  handleChange(event) {
    if (event.target.value.length > 0) {
      document.body.classList.toggle("searching", true);
    } else {
      document.body.classList.toggle("searching", false);
    }
  }

  onLinkClick(event) {
    const targetLink = new URL(event.currentTarget.href);
    if (targetLink.pathname === window.location.pathname) {
      event.preventDefault();
      document.body.classList.toggle("searching", false);
    }
  }

  render() {
    const language = window.language_code;
    const chapterIndexName = `dev_GDRPR_chapters_${language}`;
    const articlesIndexName = `dev_GDRPR_articles_${language}`;
    const sectionsIndexName = `dev_GDRPR_sections_${language}`;
    const recitalsIndexName = `dev_GDRPR_recitals_${language}`;

    return (
      <InstantSearch
        appId="OA3O0E2RHO"
        apiKey="9e85dda151c22fc5b9a830f9d9274a30"
        indexName={chapterIndexName}
      >
        <Configure hitsPerPage={5} removeWordsIfNoResults="allOptional" />
        <SearchBox
          onChange={this.handleChange.bind(this)}
          onReset={this.onEscape.bind(this)}
          onFocus={this.handleChange.bind(this)}
          autoFocus={window.matchMedia('(min-width: 991.98px)').matches}
          translations={{
            placeholder: "Search in chapters, articles, recitals, …"
          }}
        />
        <div className="search-results col-12">
          <div className="row search-top">
            <div className="col-xs-12 col-md-6 col-lg-4">
              <h3>
                <span>Chapters</span>
              </h3>
              <ConnectedChapters onLinkClick={this.onLinkClick} />
            </div>
            <div className="col-xs-12 col-md-6 col-lg-4">
              <h3>
                <span>Articles</span>
              </h3>
              <Index indexName={articlesIndexName}>
                <Configure
                  hitsPerPage={5}
                  removeWordsIfNoResults="allOptional"
                />
                <ConnectedArticles onLinkClick={this.onLinkClick} />
                <ConnectedPagination offset={3} />
              </Index>
            </div>
            <div className="col-xs-12 col-lg-4">
              <div style={{ marginTop: 70 }} className="d-lg-none"/>
              <h3>
                <span>Recitals</span>
              </h3>
              <Index indexName={recitalsIndexName}>
                <Configure
                  hitsPerPage={10}
                  removeWordsIfNoResults="allOptional"
                />
                <ConnectedRecitals onLinkClick={this.onLinkClick} />
                <ConnectedPagination offset={1} />
              </Index>
            </div>
          </div>
          <div className="row search-bottom">
            <div className="col-12">
              <h3>
                <span>Regulations</span>
              </h3>
              <Index indexName={sectionsIndexName}>
                <Configure
                  hitsPerPage={5}
                  removeWordsIfNoResults="allOptional"
                />
                <ConnectedSections onLinkClick={this.onLinkClick} />
              </Index>
            </div>
          </div>
        </div>
        <a onClick={this.onEscape.bind(this)} className="search-escape d-none d-lg-block">
          <i className="fa fa-times" />
          <br />esc
        </a>
      </InstantSearch>
    );
  }
}

const element = <Search name="test" />;
ReactDOM.render(element, document.getElementById("search"));
