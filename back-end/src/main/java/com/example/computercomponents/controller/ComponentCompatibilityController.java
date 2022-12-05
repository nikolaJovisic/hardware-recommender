package com.example.computercomponents.controller;

import com.example.computercomponents.service.ComponentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
@RequestMapping("/api/compatible")
public class ComponentCompatibilityController {

    private final ComponentService componentService;

    @Autowired
    public ComponentCompatibilityController(ComponentService componentService) {
        this.componentService = componentService;
    }

    @GetMapping("/motherboards/{componentType}/{componentName}")
    public ResponseEntity<List<String>> getCompatibleMotherboards(@PathVariable String componentName, @PathVariable String componentType){
        var response = componentService.getCompatibleMotherboards(componentName, componentType);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @GetMapping("/{motherboard}/{component}")
    public ResponseEntity<List<String>> getCompatibleComponents(@PathVariable String component,@PathVariable String motherboard){
        var response = componentService.getMotherboardCompatibleComponents(component,motherboard);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}
