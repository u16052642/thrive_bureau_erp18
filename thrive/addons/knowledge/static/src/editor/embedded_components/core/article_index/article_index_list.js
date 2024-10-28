import { Component } from "@thrive/owl";

export class ArticleIndexList extends Component {
    static template = "knowledge.ArticleIndexList";
    static props = {
        articles: { type: Object },
    };

    onArticleLinkClick(ev, articleId) {
        if (this.env.openArticle) {
            ev.preventDefault();
            ev.stopPropagation();
            this.env.openArticle(articleId);
        }
    }
}
