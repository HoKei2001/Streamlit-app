# Streamlit-app

Visit this site here:
https://hokei2001.streamlit.app/
# Use LLM to compare the overlap of academic articles  

### Nougat: Convert pdf to markdown

> Github: https://github.com/facebookresearch/nougat
>
> - This project use Nougat API run on local server
> - Once you deploy a Nougat API successfully, you can fill the  Nougat api path in Setting page. For example:  If your service run on this port,  http://127.0.0.1:8503, you can just use this path.

- Nougat, the academic document PDF parser that understands LaTeX math and tables.Project page: https://facebookresearch.github.io/nougat/

#### Install

From pip:

```
pip install nougat-ocr
```

From repository:

```
pip install git+https://github.com/facebookresearch/nougat
```

> Note, on Windows: If you want to utilize a GPU, make sure you first install the correct PyTorch version. Follow instructions [here](https://pytorch.org/get-started/locally/)

There are extra dependencies if you want to call the model from an API or generate a dataset.
Install via

`pip install "nougat-ocr[api]"` or `pip install "nougat-ocr[dataset]"`

#### Get prediction for a PDF by API

With the extra dependencies you use `app.py` to start an API. Call

```sh
$ nougat_api
```

To get a prediction of a PDF file by making a POST request to http://127.0.0.1:8503/predict/. It also accepts parameters `start` and `stop` to limit the computation to select page numbers (boundaries are included).

The response is a string with the markdown text of the document.

```sh
curl -X 'POST' \
  'http://127.0.0.1:8503/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@<PDFFILE.pdf>;type=application/pdf'
```

To use the limit the conversion to pages 1 to 5, use the start/stop parameters in the request URL: http://127.0.0.1:8503/predict/?start=1&stop=5

#### Dataset

##### Generate dataset

To generate a dataset you need 

1. A directory containing the PDFs
2. A directory containing the `.html` files (processed `.tex` files by [LaTeXML](https://math.nist.gov/~BMiller/LaTeXML/)) with the same folder structure
3. A binary file of [pdffigures2](https://github.com/allenai/pdffigures2) and a corresponding environment variable `export PDFFIGURES_PATH="/path/to/binary.jar"`

Next run

```
python -m nougat.dataset.split_htmls_to_pages --html path/html/root --pdfs path/pdf/root --out path/paired/output --figure path/pdffigures/outputs
```

Additional arguments include

| Argument              | Description                                |
| --------------------- | ------------------------------------------ |
| `--recompute`         | recompute all splits                       |
| `--markdown MARKDOWN` | Markdown output dir                        |
| `--workers WORKERS`   | How many processes to use                  |
| `--dpi DPI`           | What resolution the pages will be saved at |
| `--timeout TIMEOUT`   | max time per paper in seconds              |
| `--tesseract`         | Tesseract OCR prediction for each page     |

Finally create a `jsonl` file that contains all the image paths, markdown text and meta information.

```
python -m nougat.dataset.create_index --dir path/paired/output --out index.jsonl
```

For each `jsonl` file you also need to generate a seek map for faster data loading:

```
python -m nougat.dataset.gen_seek file.jsonl
```

The resulting directory structure can look as follows:

```
root/
├── images
├── train.jsonl
├── train.seek.map
├── test.jsonl
├── test.seek.map
├── validation.jsonl
└── validation.seek.map
```

Note that the `.mmd` and `.json` files in the `path/paired/output` (here `images`) are no longer required.
This can be useful for pushing to a S3 bucket by halving the amount of files.

#### Training

To train or fine tune a Nougat model, run 

```
python train.py --config config/train_nougat.yaml
```

#### Evaluation

Run 

```
python test.py --checkpoint path/to/checkpoint --dataset path/to/test.jsonl --save_path path/to/results.json
```

To get the results for the different text modalities, run

```
python -m nougat.metrics path/to/results.json
```

#### FAQ

- Why am I only getting `[MISSING_PAGE]`?

  Nougat was trained on scientific papers found on arXiv and PMC. Is the document you're processing similar to that?
  What language is the document in? Nougat works best with English papers, other Latin-based languages might work. **Chinese, Russian, Japanese etc. will not work**.
  If these requirements are fulfilled it might be because of false positives in the failure detection, when computing on CPU or older GPUs ([#11](https://github.com/facebookresearch/nougat/issues/11)). Try passing the `--no-skipping` flag for now.

- Where can I download the model checkpoint from.

  They are uploaded here on GitHub in the release section. You can also download them during the first execution of the program. Choose the preferred preferred model by passing `--model 0.1.0-{base,small}`

#### Citation

```
@misc{blecher2023nougat,
      title={Nougat: Neural Optical Understanding for Academic Documents}, 
      author={Lukas Blecher and Guillem Cucurull and Thomas Scialom and Robert Stojnic},
      year={2023},
      eprint={2308.13418},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```
### LangChain with LLM models

> LangChain documents: https://python.langchain.com/v0.2/docs/introduction/

If you can understand langchain's Prompt engineering approach, you can read the Q&A chain function within func.py, which is the key to this project
