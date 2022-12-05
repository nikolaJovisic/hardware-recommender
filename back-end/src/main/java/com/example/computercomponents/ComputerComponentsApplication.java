package com.example.computercomponents;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;

@SpringBootApplication
public class ComputerComponentsApplication {

	public static void main(String[] args) {
		SpringApplication.run(ComputerComponentsApplication.class, args);
	}

	@Configuration
	public class SpringFoxConfig {
		@Bean
		public Docket api() {
			Logger logger = LoggerFactory.getLogger(ComputerComponentsApplication.class);
			logger.info("Swagger started at: 'http://localhost:8080/swagger-ui.html'");
			return new Docket(DocumentationType.SWAGGER_2)
					.select()
					.apis(RequestHandlerSelectors.any())
					.paths(PathSelectors.any())
					.build();
		}
	}

}
