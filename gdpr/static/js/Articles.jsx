import React, { Component } from "react";

import { connectHits } from "react-instantsearch/connectors";
import { Highlight } from "react-instantsearch/dom";

class ArticlesHits extends Component {
  render() {
    const { hits, onLinkClick } = this.props;
    const language = window.language_code;
    return (
      <div className="article-hits">
        {hits.map(hit => {
          return (
            <div className="row chapter-row">
              <div className="col-3">
                <p className="article-index">Art {hit.index}</p>
              </div>
              <div className="col-9">
                <p className="article-name">
                  <a
                    href={`${
                      language === "en" ? "" : "/" + language
                    }/gdpr-article-${hit.index}`}
                    onClick={onLinkClick}
                  >
                    <Highlight attribute="name" hit={hit} />
                  </a>
                </p>
                <p className="chapter-name">
                  Chap {hit.chapter__index}.{" "}
                  <Highlight attribute="chapter__name" hit={hit} />
                </p>
              </div>
            </div>
          );
        })}
        {!hits.length && (
          <div className="chapter-row">
            <p className="article-name">
              <i>No results</i>
            </p>
          </div>
        )}
      </div>
    );
  }
}

const ConnectedArticles = connectHits(ArticlesHits);

export default ConnectedArticles;
