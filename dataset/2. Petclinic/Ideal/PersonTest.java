package org.springframework.samples.petclinic.evosuite.model;

import org.junit.jupiter.api.Test;
import org.junit.Assert.*;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;
import org.springframework.samples.petclinic.model.Person;
import org.springframework.samples.petclinic.evosuite.model.Person_ESTest_scaffolding;

public class PersonTest {

  @Test
  public void testGetLastNameReturningNonEmptyString()  throws Throwable  {
      Person person0 = new Person();
      person0.setLastName("Lw*`onX`MIV%");
      String string0 = person0.getLastName();
      assertEquals("Lw*`onX`MIV%", string0);
  }

  @Test
  public void testGetFirstNameReturningNonEmptyString()  throws Throwable  {
      Person person0 = new Person();
      person0.setFirstName("Lw*`onX`MIV%");
      String string0 = person0.getFirstName();
      assertEquals("Lw*`onX`MIV%", string0);
  }

  @Test
  public void testGetFirstName()  throws Throwable  {
      Person person0 = new Person();
      person0.setFirstName("George");
      String string0 = person0.getFirstName();
      assertEquals("George", string0);
  }

    @Test
  public void testGetLastName()  throws Throwable  {
      Person person0 = new Person();
      person0.setLastName("Franklin");
      String string0 = person0.getLastName();
      assertEquals("Franklin", string0);
  }

  @Test
  public void testGetFirstNameReturningEmptyString()  throws Throwable  {
      Person person0 = new Person();
      person0.setFirstName("");
      String string0 = person0.getFirstName();
      assertEquals("", string0);
  }

  @Test
  public void testGetLastNameReturningNull()  throws Throwable  {
      Person person0 = new Person();
      String string0 = person0.getLastName();
      assertNull(string0);
  }

  @Test
  public void testGetLastNameReturningEmptyString()  throws Throwable  {
      Person person0 = new Person();
      person0.setLastName("");
      String string0 = person0.getLastName();
      assertEquals("", string0);
  }

  @Test
  public void testGetFirstNameReturningNull()  throws Throwable  {
      Person person0 = new Person();
      String string0 = person0.getFirstName();
      assertNull(string0);
  }
}
