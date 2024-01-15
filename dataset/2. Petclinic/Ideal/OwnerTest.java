package org.springframework.samples.petclinic.owner;

import org.springframework.samples.petclinic.owner.Owner;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Optional;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;
import static org.mockito.BDDMockito.anyString;
import static org.mockito.BDDMockito.given;

public class OwnerTest {

    private static final int TEST_OWNER_ID = 1;
    private Owner subject;

    @BeforeEach
    public void setUp() throws Exception {
        MockitoAnnotations.openMocks(this);

        Owner subject = new Owner();
		subject.setId(TEST_OWNER_ID);
		subject.setFirstName("George");
		subject.setLastName("Franklin");
		subject.setAddress("110 W. Liberty St.");
		subject.setCity("Madison");
		subject.setTelephone("6085551023");
		Pet max = new Pet();
		PetType dog = new PetType();
		dog.setName("dog");
		max.setType(dog);
		max.setName("Max");
		max.setBirthDate(LocalDate.now());
		subject.addPet(max);
		max.setId(1);
    }

    @Test
    public void getPetsTest() throws Exception
		PersistentBag getPets = subject.getPets();

		PetType petType = new PetType();
		petType.setName("dog");
		Pet pet = new Pet();
		pet.setId(1);
		pet.setType(petType);
		pet.setBirthDate(LocalDate.now());
		pet.setName("Max");
		PersistentBag<Pet> pets = new PersistentBag<>();
		pets.add(pet);

		assertThat(getPets, is(pets));
    }

    @Test
    public void getTelephoneTest() throws Exception{
		String getTelephone = subject.getTelephone();

		assertThat(getTelephone, is("6085551023"));
    }

    @Test
    public void getAddressTest() throws Exception{
		String getAddress = subject.getAddress();

		assertThat(getAddress, is("110 W. Liberty St."));
    }

    @Test
    public void getCityTest() throws Exception{
		String getCity = subject.getCity();

		assertThat(getCity, is("Madison"));
    }

}