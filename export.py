import arcpy
from arcpy import env

parentGeodatabase = arcpy.GetParameterAsText(0)
outGeodb = arcpy.GetParameterAsText(1)
replicaName = arcpy.GetParameterAsText(2)
query = arcpy.GetParameterAsText(3)

env.workspace = parentGeodatabase
allFeatureClasses = arcpy.ListTables();
dataSets = arcpy.ListDatasets()
for dataset in dataSets:
    featureClasses = arcpy.ListFeatureClasses('*', '', dataset)
    print dataset
    arcpy.AddMessage(dataset)
    for featureClass in featureClasses:
        try:
            print featureClass
            featureNames = featureClass.split(".")
            pureName = featureNames[-1]
            arcpy.AddMessage("    " +pureName)
            arcpy.MakeFeatureLayer_management(featureClass, pureName + "_New", query, dataset)
            allFeatureClasses.append(pureName + "_New")
        except Exception, e:
            arcpy.AddError(e.message)
            # arcpy.MakeFeatureLayer_management(featureClass, featureClass + "_New", workspace=dataset)
            print ('query didnt applied to this layer ' + featureClass + " " + arcpy.GetMessages())
            pass
if len(allFeatureClasses) == 0:
    print "No layer found for replica"
    arcpy.AddMessage("No layer found for replica")
else:
    arcpy.AddMessage("Starting replica creation")
    arcpy.CreateReplica_management(allFeatureClasses, 'CHECK_OUT', outGeodb, replicaName)
    arcpy.AddMessage("Replica Completed")
