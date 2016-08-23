package org.insightedge.pythondemo;

import org.apache.spark.api.java.JavaSparkContext;
import org.insightedge.spark.context.InsightEdgeSparkContext;
import org.insightedge.spark.mllib.MLInstance;

public class PythonInsightEdgeSparkContext {

    private InsightEdgeSparkContext ieContext;

    public void init(JavaSparkContext jsc) {
        this.ieContext = new InsightEdgeSparkContext(jsc.sc());
    }

    public void saveMlInstance(String name, Object model) {
        ieContext.grid().write(new MLInstance(name, model));
    }

    public Object loadMlInstance(String name, String className) {
        try {
            Class clazz = Class.forName(className);
            MLInstance mlModel = ieContext.grid().readById(MLInstance.class, name);
            return clazz.cast(mlModel.getInstance());
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("Could not find class", e);
        }
    }

}
