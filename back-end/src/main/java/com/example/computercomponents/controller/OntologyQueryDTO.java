package com.example.computercomponents.controller;
//(String componentType,String currentComponentName,String motherboard)
public class OntologyQueryDTO {
    private String componentType;
    private String currentComponentName;
    private String motherboard;

    public OntologyQueryDTO() {
    }

    public String getComponentType() {
        return componentType;
    }

    public void setComponentType(String componentType) {
        this.componentType = componentType;
    }

    public String getCurrentComponentName() {
        return currentComponentName;
    }

    public void setCurrentComponentName(String currentComponentName) {
        this.currentComponentName = currentComponentName;
    }

    public String getMotherboard() {
        return motherboard;
    }

    public void setMotherboard(String motherboard) {
        this.motherboard = motherboard;
    }
}
