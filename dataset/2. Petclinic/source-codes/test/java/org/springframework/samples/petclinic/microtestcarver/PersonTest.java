package org.springframework.samples.petclinic.microtestcarver;

import org.springframework.samples.petclinic.model.Person;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class PersonTest {

    private Person subject;

    @Before
    public void setUp() throws Exception {
        subject = new Person();

		subject.setId(1);
		subject.setFirstName("George");
		subject.setLastName("Franklin");

    }

    @Test
    public void getFirstName(){
		String getFirstName = subject.getFirstName();

		assertEquals(getFirstName, "George");
    }

	@Test
	public void GetLastName(){
		String getLastName = subject.getLastName();

		assertEquals(getLastName, "Franklin");
	}

}
