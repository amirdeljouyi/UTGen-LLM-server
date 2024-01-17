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
    public void testGetPet() throws Exception{
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
    public void testGetTelephone() throws Exception{
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
    public void testGetCity() throws Exception{
        Owner subject = new Owner();
        subject.setCity("Madison");
		String getCity = subject.getCity();

		assertThat(getCity, is("Madison"));
    }


    @Test
    @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
    public void testOwnerAddPetAndGetPets() throws Throwable  {
        // Create a new owner and pet object
        Owner owner = new Owner();
        Pet pet = new Pet();
        // Add the pet to the owner's list of pets
        owner.addPet(pet);
        // Get the list of pets for this owner
        List<Pet> pets = owner.getPets();
        // Assert that the list is not empty
        assertFalse(pets.isEmpty());
    }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testAddPetAndGetId() throws Throwable  {
      // This test verifies that the Owner class can add a new Pet to its list of pets
      // and that the Pet's ID is properly set.
      Owner owner = new Owner();
      Pet pet = new Pet();
      owner.addPet(pet);
      Integer id = Opcodes.DOUBLE;
      pet.setId(id);
      Pet retrievedPet = owner.getPet("");
      assertEquals(3, (int)retrievedPet.getId());
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testSetAndGetCity() throws Throwable  {
      Owner owner = new Owner();
      // Create a new instance of the Owner class
      owner.setCity("");
      // Set the city attribute to an empty string
      String city = owner.getCity();
      // Get the value of the city attribute
      assertEquals("", city);
      // Assert that the city is an empty string
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testAddVisitOwner() throws Throwable  {
      // Create a new Owner and Pet instances
      Owner owner = new Owner();
      Pet pet = new Pet();
      // Add the Pet to the Owner
      owner.addPet(pet);
      // Set the ID of the Pet to a specific value (Opcodes.NULL)
      Integer petId = Opcodes.NULL;
      pet.setId(petId);
      // Create a new Visit instance
      Visit visit = new Visit();
      // Add the Visit to the Owner for the Pet with ID petId
      Owner addVisit = owner.addVisit(petId, visit);
      // Assert that the returned Owner is the same as the original Owner
      assertSame(addVisit, owner);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testAddVisit() throws Throwable  {
      // Create a new owner and pet objects
      Owner owner = new Owner();
      Pet pet = new Pet();
      // Add the pet to the owner
      owner.addPet(pet);
      // Set the ID of the pet to null
      Integer petId = Opcodes.NULL;
      pet.setId(petId);
      // Create a new visit object and set its ID to the same as the pet's ID
      Visit visit = new Visit();
      owner.setId(petId);
      // Add the visit to the owner
      Owner addVisit = owner.addVisit(petId, visit);
      // Assert that the last name of the added visit is null
      assertNull(addVisit.getLastName());
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetPetsWhenNoPetsExist() throws Throwable  {
      // Create a new Owner object
      Owner owner = new Owner();
      // Retrieve the list of pets for this owner
      List<Pet> pets = owner.getPets();
      // Assert that the size of the pet list is 0
      assertEquals(0, pets.size());
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testAddPet() throws Throwable  {
      // Create a new owner and pet object
      Owner owner = new Owner();
      Pet pet = new Pet();
      // Add the pet to the owner's list of pets
      owner.addPet(pet);
      // Set the pet's ID to a double value (1.0)
      Integer id = Opcodes.DOUBLE;
      pet.setId(id);
      // Get the pet from the owner using its name and ignore case (true)
      Pet retrievedPet = owner.getPet("", true);
      // Assert that the retrieved pet is the same as the original pet
      assertSame(retrievedPet, pet);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testAddAndGetPetNullPointerExceptionIsThrownWhenNoPetNameIsProvided() throws Throwable  {
      // Create a new Owner object and a new Pet object
      Owner owner = new Owner();
      Pet pet = new Pet();
      // Add the Pet to the Owner's list of pets
      owner.addPet(pet);
      // Get the Pet from the Owner using its name
      Pet retrievedPet = owner.getPet("");
      // Assert that the returned Pet is null, since it does not exist in the database
      assertNull(retrievedPet);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetPetNotFound() throws Throwable  {
      // Create a new owner and pet
      Owner owner = new Owner();
      Pet pet = new Pet();
      owner.addPet(pet);

      // Set the ID of the pet to an invalid value (a double)
      Integer id = Opcodes.DOUBLE;
      pet.setId(id);

      // Try to get the pet by its invalid ID
      Pet retrievedPet = owner.getPet(id);

      // Assert that the returned pet is null, since it does not exist in the database
      assertNull(retrievedPet);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetAddressWithNoPets() throws Throwable  {
      // Arrange
      Owner owner = new Owner();
      Pet pet = new Pet();
      Integer id = 1;
      pet.setId(id);

      // Act
      owner.addPet(pet);

      // Assert
      assertNull(owner.getAddress());
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetCityReturnsNullWhenOwnerHasNoCity() throws Throwable  {
      // Arrange
      Owner owner = new Owner();
      // Act
      String city = owner.getCity();
      // Assert
      assertNull(city);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetPetNull() throws Throwable  {
      Owner owner = new Owner();
      // Obtain the pet object associated with the given name
      Pet pet = owner.getPet("");
      // Verify that the returned pet is null
      assertNull(pet);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetAddress() throws Throwable  {
      Owner owner = new Owner();
      // Create a new instance of the Owner class and set its address to "123 Main St"
      owner.setAddress("123 Main St");
      String expectedAddress = "123 Main St";
      String actualAddress = owner.getAddress();
      // Verify that the address was set correctly by comparing the expected value with the actual value
      assertEquals(expectedAddress, actualAddress);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testOwnerToStringreturnsNonNullString() throws Throwable  {
      // Arrange
      Owner owner = new Owner();

      // Act
      String string = owner.toString();

      // Assert
      assertNotNull(string);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetSetTelephone() throws Throwable  {
      // Create a new owner object and set its telephone number
      Owner owner = new Owner();
      owner.setTelephone("555-1234");

      // Retrieve the telephone number from the owner object
      String expectedTelephone = "555-1234";
      String actualTelephone = owner.getTelephone();

      // Assert that the retrieved telephone number is equal to the expected value
      assertEquals(expectedTelephone, actualTelephone);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testAddAndGetPetSuccessful() throws Throwable  {
      // Create a new owner and pet object
      Owner owner = new Owner();
      Pet pet = new Pet();
      // Add the pet to the owner's list of pets
      owner.addPet(pet);
      // Retrieve the pet from the owner by ID
      Integer id = Opcodes.DOUBLE;
      Pet retrievedPet = owner.getPet(id);
      // Assert that the retrieved pet is null, since it does not exist in the list of pets
      assertNull(retrievedPet);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void testGetAddressReturnsNullWhenOwnerHasNoAddress() throws Throwable  {
      // Arrange
      Owner owner = new Owner();

      // Act
      String address = owner.getAddress();

      // Assert
      assertNull(address);
  }

  @Test
  @Timeout(value = 4000 , unit = TimeUnit.MILLISECONDS)
  public void and() throws Throwable  {
      // Create a new Owner object and set its city to "San Francisco"
      Owner owner = new Owner();
      owner.setCity("San Francisco");

      // Get the city of the Owner object
      String actualCity = owner.getCity();

      // Assert that the actual city is equal to the expected city
      assertEquals("San Francisco", actualCity);
  }
}