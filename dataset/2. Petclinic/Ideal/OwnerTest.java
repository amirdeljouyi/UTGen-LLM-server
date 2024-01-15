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

    @Test
    public void getPetsTest() throws Exception{
        Owner subject = new Owner();
        Pet max = new Pet();
		PetType dog = new PetType();
		dog.setName("dog");
		max.setType(dog);
		max.setName("Max");
		max.setBirthDate(LocalDate.now());
		max.setId(1);
		subject.addPet(max);

		Pet getPet = subject.getPet("Max");

		assertThat("Max", getPet.toString());
    }

    @Test
    public void getTelephoneTest() throws Exception{
        Owner subject = new Owner();
        subject.setTelephone("6085551023");

		String getTelephone = subject.getTelephone();

		assertThat(getTelephone, is("6085551023"));
    }

    @Test
    public void getAddressTest() throws Exception{
        Owner subject = new Owner();
        subject.setAddress("110 W. Liberty St.");
		String getAddress = subject.getAddress();

		assertThat(getAddress, is("110 W. Liberty St."));
    }

    @Test
    public void getCityTest() throws Exception{
        Owner subject = new Owner();
        subject.setCity("Madison");
		String getCity = subject.getCity();

		assertThat(getCity, is("Madison"));
    }

}