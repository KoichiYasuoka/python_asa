from asapy.result.Result import Result
from asapy.result.Chunk import Chunk
from asapy.result.Morph import Morph


class Analyzer():

    def __init__(self, analyzertype: str, code: str) -> None:
        if analyzertype == 'cabocha':
            import CaboCha
            self.analyzer = CaboCha.Parser("-f1 -n1")
            self.to_list = lambda tree: tree.toString(CaboCha.FORMAT_LATTICE).split("\n")
        elif analyzertype == 'ginza':
            import spacy
            from ginza.command_line import analyze_cabocha
            self.analyzer = type('',(object,),{'parse':spacy.load('ja_ginza')})
            self.to_list = lambda tree: self.pos_change([t for s in tree.sents for t in analyze_cabocha(s)])
        else:
            import unidic2ud.cabocha as CaboCha
            self.analyzer = CaboCha.Parser(analyzertype)
            self.to_list = lambda tree: self.pos_change(tree.toString(CaboCha.FORMAT_LATTICE).split("\n"))

    def parse(self, line: str) -> Result:
        m_id = 0
        result = Result(line)
        tree = self.analyzer.parse(line)
        line_list = self.to_list(tree)
        for line in line_list:
            if line == "EOS":
                break
            if line.startswith("* "):
                result.addChunk(Chunk(line))
                m_id = 0
            elif line != "EOS":
                result.chunks[-1].addMorph(Morph(m_id, line))
                m_id += 1
        return result

    def pos_change(self, tree):
        r = []
        for t in tree:
            d = t.split("\t")
            if len(d) == 1:
                m = d[0].split()
                if len(m) > 3:
                    if m[0] == "*":
                        h = int(m[3].split("/")[0])
                        i = 0
            elif len(d) > 1:
                m = d[1].split(",")
                if m[0] == "動詞":
                    m[1] = "自立" if i == h else "非自立"
                elif m[0] == "助動詞":
                    m[4] = "判定詞" if m[6] in {"だ", "です"} else m[4]
                d[1] = ",".join(m)
                i += 1
            r.append("\t".join(d))
        return r
