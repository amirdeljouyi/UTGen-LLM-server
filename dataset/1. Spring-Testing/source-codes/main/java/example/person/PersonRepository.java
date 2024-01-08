package example.person;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.transaction.annotation.Transactional;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Optional;

public interface PersonRepository extends CrudRepository<Person, String>, Serializable {

    Optional<Person> findByLastName(String lastName);

//    ArrayList<Person> findAll();

    @Query("SELECT person FROM Person person")
    @Transactional(readOnly = true)
    Page<Person> findAll(Pageable pageable);

}
