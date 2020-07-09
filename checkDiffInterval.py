from DataCollecting import getTraingSetAndTestSet
from pca import do_pca_for_training_data

trainingSet, testSet=getTraingSetAndTestSet()
res, U, pcaModal=do_pca_for_training_data(trainingSet)
utest,restest=pcaModal.transform_case_obj(testSet)
print(restest)
