package example;

import example.person.Person;
import example.person.PersonRepository;
import example.weather.WeatherClient;
import example.weather.WeatherResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
public class ExampleController implements Serializable {

    private final PersonRepository personRepository;
    private final WeatherClient weatherClient;

    @Autowired
    public ExampleController(final PersonRepository personRepository, final WeatherClient weatherClient) {
        this.personRepository = personRepository;
        this.weatherClient = weatherClient;
    }

    @GetMapping("/hello")
    public String hello() {
        return "Hello World!";
    }

    @GetMapping("/hello/{lastName}")
    public String hello(@PathVariable final String lastName) {
        Optional<Person> foundPerson = personRepository.findByLastName(lastName);

        return foundPerson
                .map(person -> String.format("Hello %s %s!", person.getFirstName(), person.getLastName()))
                .orElse(String.format("Who is this '%s' you're talking about?", lastName));
    }

//    @GetMapping("/hello/all")
//    public String helloAll() {
//        int pageSize = 5;
//        int page = 1;
//
//        Pageable pageable = PageRequest.of(page - 1, pageSize);
//        Page<Person> listPersons = personRepository.findAll(pageable);
//
////        ArrayList<Person> listPersons = personRepository.findAll();
//
//        String result = "";
//
////        System.out.println(listPersons);
//        for(Person person: listPersons){
//            result = result.concat(String.format("Hello %s %s! \n\n", person.getFirstName(), person.getLastName()));
//        };
//
////        System.out.println(result);
//
//        return result;
//    }

    @GetMapping("/weather")
    public String weather() {
        return weatherClient.fetchWeather()
                .map(WeatherResponse::getSummary)
                .orElse("Sorry, I couldn't fetch the weather for you :(");
    }
}
