/*
 * This file was automatically generated by EvoSuite
 * Fri Aug 05 10:24:08 GMT 2022
 */

package example.weather;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import example.weather.WeatherResponse;
import java.util.List;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true) 
public class WeatherResponse_ESTest extends WeatherResponse_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void testGetSummary()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse("Jy(+XI9N", "Jy(+XI9N");
      String string0 = weatherResponse0.getSummary();
      assertEquals("Jy(+XI9N: Jy(+XI9N", string0);
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherTakingNoArgumentsAndCallsEquals0()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather();
      WeatherResponse.Weather weatherResponse_Weather1 = new WeatherResponse.Weather();
      boolean boolean0 = weatherResponse_Weather0.equals(weatherResponse_Weather1);
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherTaking2ArgumentsAndCallsEquals0()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather("&_>!@K", "&_>!@K");
      WeatherResponse.Weather weatherResponse_Weather1 = new WeatherResponse.Weather("S:q$ZHC!0J3", "&_>!@K");
      boolean boolean0 = weatherResponse_Weather0.equals(weatherResponse_Weather1);
      assertFalse(boolean0);
      assertEquals("&_>!@K", weatherResponse_Weather1.getDescription());
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherTaking2ArgumentsAndCallsEquals1()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather("&_>!@K", "&_>!@K");
      WeatherResponse.Weather weatherResponse_Weather1 = new WeatherResponse.Weather("&_>!@K", "S:q$ZHC!0J3");
      boolean boolean0 = weatherResponse_Weather1.equals(weatherResponse_Weather0);
      assertFalse(boolean0);
      assertEquals("Weather{main='&_>!@K', description='S:q$ZHC!0J3'}", weatherResponse_Weather1.toString());
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherTaking2ArgumentsAndCallsEquals2()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather("&_>!@K", "&_>!@K");
      boolean boolean0 = weatherResponse_Weather0.equals((Object) null);
      assertFalse(boolean0);
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherTaking2ArgumentsAndCallsEquals3()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather("&_>!@K", "&_>!@K");
      Object object0 = new Object();
      boolean boolean0 = weatherResponse_Weather0.equals(object0);
      assertFalse(boolean0);
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherResponseTakingNoArgumentsAndCallsEquals0()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse();
      WeatherResponse weatherResponse1 = new WeatherResponse();
      boolean boolean0 = weatherResponse1.equals(weatherResponse0);
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void testEqualsWithNull()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse("S:q$ZHC!0J3", "&_>!@K");
      boolean boolean0 = weatherResponse0.equals((Object) null);
      assertFalse(boolean0);
      assertEquals("WeatherResponse{weather=[Weather{main='S:q$ZHC!0J3', description='&_>!@K'}]}", weatherResponse0.toString());
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherResponseTakingNoArgumentsAndCallsEquals1()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse();
      boolean boolean0 = weatherResponse0.equals(weatherResponse0);
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void testEqualsReturningFalse()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse();
      boolean boolean0 = weatherResponse0.equals("");
      assertFalse(boolean0);
  }

  @Test(timeout = 4000)
  public void testGetWeather()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse();
      List<WeatherResponse.Weather> list0 = weatherResponse0.getWeather();
      assertNull(list0);
  }

  @Test(timeout = 4000)
  public void testGetSummaryThrowsNullPointerException()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse();
      // Undeclared exception!
      try { 
        weatherResponse0.getSummary();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("example.weather.WeatherResponse", e);
      }
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherResponseTaking2ArgumentsAndCallsToString()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse("", "");
      String string0 = weatherResponse0.toString();
      assertEquals("WeatherResponse{weather=[Weather{main='', description=''}]}", string0);
  }

  @Test(timeout = 4000)
  public void testGetMain()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather("&_>!@K", "&_>!@K");
      String string0 = weatherResponse_Weather0.getMain();
      assertEquals("&_>!@K", string0);
  }

  @Test(timeout = 4000)
  public void testHashCode()  throws Throwable  {
      WeatherResponse weatherResponse0 = new WeatherResponse("^&1^eTw!cz$D?NG]#", "^&1^eTw!cz$D?NG]#");
      weatherResponse0.hashCode();
  }

  @Test(timeout = 4000)
  public void testGetDescription()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather("&_>!@K", "&_>!@K");
      String string0 = weatherResponse_Weather0.getDescription();
      assertEquals("&_>!@K", string0);
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherTaking2ArgumentsAndCallsToString()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather("&_>!@K", "&_>!@K");
      String string0 = weatherResponse_Weather0.toString();
      assertEquals("Weather{main='&_>!@K', description='&_>!@K'}", string0);
  }

  @Test(timeout = 4000)
  public void testCreatesWeatherTakingNoArgumentsAndCallsEquals1()  throws Throwable  {
      WeatherResponse.Weather weatherResponse_Weather0 = new WeatherResponse.Weather();
      boolean boolean0 = weatherResponse_Weather0.equals(weatherResponse_Weather0);
      assertTrue(boolean0);
  }
}