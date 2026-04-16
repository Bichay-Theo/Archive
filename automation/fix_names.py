name: "تَصْحِيحُ الأَسْمَاءِ وَتَعْمِيدُ الرَّوَابِطِ"

on:
  workflow_dispatch: # هـذا مـا يـَجـعـَلـُه يـَظـهـَرُ كـَـزِرٍّ يـَدَوِيّ

permissions:
  contents: write # مـَنـحُ الـسـِّيـادَةِ لـِلـكـِتـابـَةِ فـِي الـمـُسـتـَودَع

jobs:
  fix-and-clean:
    runs-on: ubuntu-latest
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
    steps:
      - uses: actions/checkout@v4
      
      - name: "تـَهـيـِئـَةُ الـبـِيـئـَة"
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: "تـَنـفـِيـذُ الـتـَّطـهـِيـرِ الـرَّقـْمـِي"
        run: python automation/fix_names.py
        
      - name: "حـَفـظُ الـتـَّغـيـِيـراتِ الـنـِّهـائـِيـَّة"
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          git add .
          git commit -m "تَصْحِيحُ مِعْمَارِ الأَسْمَاءِ [حَسْمُ مَشَاكِلِ 404]" || echo "لا توجد تغييرات"
          git push
