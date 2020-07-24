import spacy
from spacy.tokens import Span
import re

class RuleBuilder:
    """Build rule for Entity Ruler based on concept's label, id and a rule level (strict, common or permis)"""

    LANGSENT = {
        'fr': {
            'sent': 'Le %s est une entité nommée.',
            'size': 5
        }
    }
    OPTADJ = {"pos": "ADJ", "OP": "*"}

    def __init__(self, cfg):
        self.lang = cfg.get('language')
        self.lvlfunc = {
            'strict': self.build_strict_rule,
            'common': self.build_common_rule,
            'permis': self.build_permis_rule,
            'regexp': self.build_regexp_rule
        }
        self.sent = __class__.LANGSENT[self.lang]

        self.nlp = spacy.load(cfg.get('model'))
        self.nlp.remove_pipe('ner')

    def __call__(self, nes):
        """Build a set of rules from a list of named entities, labels and a rule level."""
        rules = []
        for ne in nes:
            func = self.lvlfunc[ne['level']]
            rules.append(func(ne))
            func = self.lvlfunc['regexp']
            rules.append(func(ne))
        return rules

    def build_strict_rule(self, ne):
        """Build a rule matching the exact string."""
        id_ = ne['id']
        label = ne['label']
        pattern = '%s' % ne['entity']
        return {"id": id_, "label": label, "pattern": pattern}

    def build_common_rule(self, ne):
        """Build a rule matching ne's part-of-speech and lemmas annotations."""
        id_ = ne['id']
        label = ne['label']
        entitysent = self.sent['sent'] % ne['entity']
        doc = self.nlp(entitysent)

        wdps = []
        for token in doc[1:len(doc) - self.sent['size']]:
            wdps.append({"pos": token.pos_, "lemma": token.lemma_})
        pattern = wdps
        return {"id": id_, "label": label, "pattern": pattern}

    def build_permis_rule(self, ne):
        """Build a rule matching any noun groups which main noun is ne's noun and where ne's qualifiers are
        among main noun's qualifiers. It uses part-of-speech and lemmas annotations to function.
        TODO : see if Entity Rules can use dependencies annotations"""
        id_ = ne['id']
        label = ne['label']
        entitysent = self.sent['sent'] % ne['entity']
        doc = self.nlp(entitysent)

        wdps = []
        for token in doc[1:len(doc) - self.sent['size']]:
            if token.pos_ in {"NOUN","PROPN"}:
                wdps.append({"pos": {"IN" : ["NOUN" ,"PROPN"]}, "lemma": token.lemma_})
            else:
                wdps.append({"pos": token.pos_, "lemma": token.lemma_})
            wdps.append(__class__.OPTADJ)
        pattern = wdps
        return {"id": id_, "label": label, "pattern": pattern}

    def build_regexp_rule(self, ne):
        """Build a rule matching regular expression."""
        id_ = ne['id']
        label = ne['label']
        p = re.compile('\s*\([a-zA-Z0-9_\s]*\)')
        pattern=p.sub('', ne['entity'])
        return {"id": id_, "label": label, "pattern": pattern}

    def get_pipeline(self):
        """Get pipeline"""
        return self.nlp


class EntityLinker:

    def __init__(self, cfg):
        # TODO fix force=True (isn't supposed to work that way)
        self.__name__ = 'linker'
        Span.set_extension("link", default=None, force=True)
        self.LABEL_URL_MAPPER = cfg['EntityLinker']

    def __call__(self, doc):
        for ent in doc.ents:
            if ent.label_ in self.LABEL_URL_MAPPER.keys():
                ent._.link = self.LABEL_URL_MAPPER.get(ent.label_) + ent.ent_id_
        return doc
