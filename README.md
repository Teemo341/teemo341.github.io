# Shiyu Shen / 沈石禹 · Academic Homepage

默认英文，右上角可切换中文。网页和两份 LaTeX 共用 `content.json`，论文标题在网页及 PDF 中均为黑色超链接。

- 主页：https://teemo341.github.io/
- 中文：https://teemo341.github.io/zh/
- 英文简历：[LaTeX](cv/Shiyu_Shen_Academic_CV.tex) · [PDF](cv/Shiyu_Shen_Academic_CV.pdf)
- 中文简历：[LaTeX](cv/Shiyu_Shen_Academic_CV_CN.tex) · [PDF](cv/Shiyu_Shen_Academic_CV_CN.pdf)

## 以后通过对话更新

提供此仓库链接和新的事实即可，例如：“新增一篇论文，题目……，作者……，2027 年录用到……，链接……；请同步更新中英文主页、两份 LaTeX 和 PDF。”

维护要求已写入 [AGENTS.md](AGENTS.md)。先修改 `content.json`，然后生成、编译、检查并提交所有结果。原英文 TeX 用作排版参考；中文 TeX 依据所提供的中文 PDF 重建。履历、论文年份、作者顺序及在审状态没有因链接检索而擅自变更。

## 使用本地论文 PDF

1. 将真实论文 PDF 上传到 [`papers/`](papers/)，建议使用英文字母、数字和连字符命名。
2. 找到 `content.json` 中对应论文，设置 `"pdf": "papers/your-paper.pdf"`。
3. 重新生成网页及两份 LaTeX/PDF，并提交。通过对话告诉我“这篇论文使用刚上传的 PDF”也可以。

例如第 12 篇将来上传到 `papers/distribution-free-bayesian-dg.pdf` 后，将该论文的 `pdf` 字段设置为此路径即可。当前没有放置假 PDF 或不存在的下载链接。

优先顺序：**明确指定的本地 PDF → 已核实的原文 `url` → Google Scholar 精确题名检索**。清空 `pdf` 可恢复公开原文链接。配置文件不存在、不是 PDF 或路径跳出 `papers/` 时，构建会报错。网页使用相对路径，下载版简历使用对应的公开 HTTPS 地址，便于把简历发给别人后继续点击。公开 PDF 地址须在 Pages 发布后才能访问。

## 链接核验

2026-09-12 对全部 12 篇论文尝试 Google Scholar 题名检索；直接访问受到限制，使用出版商、arXiv、OpenReview 和作者机构页面核实原文。11 篇已找到原文记录。第 12 篇 **A Distribution-Free Efficient Bayesian Framework for Domain Generalization** 暂无准确公开记录，使用 Scholar 精确题名检索作为临时入口，可改为用户提供的 PDF；检索链接不意味着已被 Scholar 收录。

第 6 篇 **Contrastive Heliophysical Image Pretraining for Solar Dynamics Observatory Records** 的 [arXiv 记录](https://arxiv.org/abs/2511.22958)目前标记撤回，当前页面无 PDF。保留记录页，用户可指定新版链接或本地 PDF。逐篇来源和访问限制见 [publication-link-audit.json](docs/publication-link-audit.json)。

## 生成与检查

网页与 LaTeX 生成只需 Python 3.10+：

```bash
python3 scripts/build.py
```

编译两份 PDF 需带中文支持的 XeLaTeX / TeX Live（含 xeCJK 及 Fandol 或 Noto CJK 字体）；西文字体支持 TeX Gyre Heros、Arimo，也可回退到 Latin Modern Sans：

```bash
python3 scripts/build.py --pdf
python3 scripts/check.py --pdf
python3 -m unittest discover -s tests
```

`check.py --pdf` 需要 Python `pypdf`；不加 `--pdf` 时检查网页与链接路径。生成的 `.tex` 是完整文档，可在 `cv/` 内单独编译；照片通过 `../assets/portrait.jpg` 引用，在其他 LaTeX 环境使用时应保留这个路径或修改模板。

内容修改 `content.json`；CV 排版修改 `scripts/render_cv.py` 或 `templates/` 下模板；网页样式修改 `assets/style.css`。不要只改生成的 HTML 或 TeX，下次生成会覆盖。预览：在根目录运行 `python3 -m http.server 8000`，访问 http://localhost:8000 。

## GitHub Pages

仓库名为 `teemo341.github.io`，主页直接发布在根域名 `https://teemo341.github.io/`。在 **Settings → Pages → Build and deployment** 选择 **Deploy from a branch → main → /(root) → Save**。启用后，推送生成的静态网页即可触发发布。[GitHub 官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

迁移域名或修改仓库名称时，更新 `site.base_url` 并重新生成网页与两份 CV，检查本地论文 PDF 链接。网站无需数据库或外部字体 CDN。
