from Domain.BCExtractorService.Classifier.LogicBasedClassifier.CovalentClassifier import ClassifierLogic

class AvaxClassifier(ClassifierLogic):
    def __init__(self, data, TokenMetaData):
       ClassifierLogic.__init__(self, data, TokenMetaData)