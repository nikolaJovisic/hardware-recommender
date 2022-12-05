package com.example.computercomponents.controller;

import com.example.computercomponents.service.ComponentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
@RequestMapping("/api/properties")
public class ComponentPropertiesComponent {

    private final ComponentService componentService;

    @Autowired
    public ComponentPropertiesComponent(ComponentService componentService) {
        this.componentService = componentService;
    }

    @PostMapping("/{componentName}/{propertyName}")
    ResponseEntity<List<String>> getPropertyValue(@PathVariable String componentName, @PathVariable String propertyName){
        var response = componentService.getComponentProperty(componentName,propertyName);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @PostMapping("/better/{componentName}/{dataProperty}")
    public ResponseEntity<List<String>> getBetterComponents(@PathVariable String componentName,@PathVariable String dataProperty){
        var response = componentService.getBetterComponents(componentName, dataProperty);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}
