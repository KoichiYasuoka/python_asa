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
            self.to_list = lambda tree: [t.replace("\t動詞,一般,", "\t動詞,自立,") for t in analyze_cabocha(tree)]
        else:
            import unidic2ud.cabocha as CaboCha
            self.analyzer = CaboCha.Parser(analyzertype)
            self.to_list = lambda tree: tree.toString(CaboCha.FORMAT_LATTICE).replace("\t動詞,一般,", "\t動詞,自立,").split("\n")

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
