# medias.pt

Consulta as médias de entrada nos cursos superiores portugueses, de 2016 a 2025 (Fase 1 do Concurso Nacional de Acesso).

**→ [medias.pt](https://medias.pt)**

## Dados

Os dados são retirados dos ficheiros oficiais publicados pela [DGES](https://www.dges.gov.pt), que contêm as notas mínimas de acesso por curso e universidade em cada ano.

## Correr localmente

```bash
npm install
npm run dev
```

O site fica disponível em `http://localhost:4321`.

## Atualizar os dados

1. Descarrega o ficheiro da DGES para `scraper/` (ex: `fase1_26.xlsx`)
2. Adiciona o novo ano ao dicionário `files` em `scraper/scraper.py`
3. Corre o scraper:

```bash
cd scraper
python scraper.py
```

4. O ficheiro `src/data/courses.json` é atualizado automaticamente.
