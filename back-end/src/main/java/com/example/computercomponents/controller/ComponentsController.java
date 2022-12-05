package com.example.computercomponents.controller;

import com.example.computercomponents.service.ComponentService;
import com.example.computercomponents.service.OntologyQueryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
@RequestMapping(value = "/api/components")
public class ComponentsController {


    private final ComponentService componentservice;
    private final OntologyQueryService queryService;

    @Autowired
    public ComponentsController(ComponentService componentservice, OntologyQueryService queryService) {
        this.componentservice = componentservice;
        this.queryService = queryService;
    }


    @PostMapping()
    public ResponseEntity<List<String>> performQuery(@RequestBody String query){
        var response = queryService.executeQuery(query);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @PostMapping("/upgrade")
    public ResponseEntity<List<String>> upgrade(@RequestBody OntologyQueryDTO ontologyQueryDTO){
        var response = componentservice.recommendUpgrade(ontologyQueryDTO.getComponentType(),ontologyQueryDTO.getCurrentComponentName(),ontologyQueryDTO.getMotherboard());
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @GetMapping("/{componentName}")
    public ResponseEntity<List<String>> getComponents(@PathVariable String componentName){
        var response = componentservice.getComponents(componentName);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }


}
