package com.example.computercomponents.service;

import com.example.computercomponents.constants.URL;
import com.fasterxml.jackson.core.type.TypeReference;
import org.apache.jena.ontology.*;
import org.apache.jena.rdf.model.Literal;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.riot.Lang;
import org.apache.jena.riot.RDFDataMgr;

import java.io.*;
import java.util.Iterator;
import java.util.Locale;
import java.util.regex.Pattern;

import com.opencsv.CSVReader;


public class PopulizationService {
    private static String preprocessName(String name) {
        return name.replaceAll("[^A-Za-z0-9]", "_").toLowerCase(Locale.ROOT);
    }
    public static void populize(String csvPath) {
        String SOURCE = "C:\\Users\\paracelsus\\Desktop\\vivodyne-diffine\\hardware-recommender\\back-end\\src\\main\\resources\\ont\\classesAndInstances.owl";
        String importNS = "http://www.semanticweb.org/paracelsus/ontologies/2022/4/untitled-ontology-3#";
        String baseNS = "http://www.semanticweb.org/pc/ontologies/2022/4/untitled-ontology-17#";

        Model base = ModelFactory.createDefaultModel();
        try {
            InputStream is = TypeReference.class.getResourceAsStream(URL.CLASSES_AND_INSTANCES_PATH);
            RDFDataMgr.read(base, is, Lang.TURTLE);
            is.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        OntModel model = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM_MICRO_RULE_INF, base);
        OntClass cpu = model.getOntClass(importNS + "CPU");
        OntClass ram = model.getOntClass(importNS + "RAM");
        OntClass motherboard = model.getOntClass(importNS + "Motherboard");
        OntClass namedIndividual = model.getOntClass("http://www.w3.org/2002/07/owl#NamedIndividual");

        OntProperty compatibleCPU = model.getOntProperty(importNS + "compatibleCPU");
        OntProperty compatibleRAM = model.getOntProperty(importNS + "compatibleRAM");


        CSVReader reader = null;
        try {
            reader = new CSVReader(new FileReader(csvPath));
            String[] nextLine;
            reader.readNext();
            int i = 50;
            while ((nextLine = reader.readNext()) != null && i-- > 0) {
                String cpu_name = baseNS + preprocessName(nextLine[0]);
                String ram_name = baseNS + preprocessName(nextLine[1]);
                String motherboard_name = baseNS + preprocessName(nextLine[2]);

                Individual motherboard_individual = model.getIndividual(motherboard_name);
                if (motherboard_individual == null) {
                    motherboard_individual = model.createIndividual(motherboard_name, motherboard);
                    motherboard_individual.addRDFType(namedIndividual);
                }

                Individual cpu_individual = model.getIndividual(cpu_name);
                if (cpu_individual == null) {
                    cpu_individual = model.createIndividual(cpu_name, cpu);
                    cpu_individual.addRDFType(namedIndividual);
                }
                cpu_individual.addProperty(compatibleCPU, motherboard_individual);

                Individual ram_individual = model.getIndividual(ram_name);
                if (ram_individual == null) {
                    ram_individual = model.createIndividual(ram_name, ram);
                    ram_individual.addRDFType(namedIndividual);
                }
                ram_individual.addProperty(compatibleRAM, motherboard_individual);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        FileWriter out = null;
        try {
            out = new FileWriter(SOURCE);
            model.write(out, "Turtle");
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (out != null) {
                try {
                    out.close();
                } catch (IOException ignore) {
                }
            }
        }

    }
}