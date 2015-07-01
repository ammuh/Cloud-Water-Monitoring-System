package com.fluxplant;
import com.google.api.server.spi.config.Api;
import com.google.api.server.spi.config.ApiMethod;
import com.google.api.server.spi.config.ApiNamespace;
import com.google.api.server.spi.config.ApiMethod.HttpMethod;
import com.google.api.server.spi.response.UnauthorizedException;
import javax.inject.Named;
/**
  * Add your first API methods in this class, or you may create another class. In that case, please
  * update your web.xml accordingly.
 **/

@Api(name = "myApi",
version = "v1",
namespace = @ApiNamespace(ownerDomain = "flux-plant.appspot.com", ownerName = "flux-plant.appspot.com", packagePath=""))

public class FluxPlantAPI {
@ApiMethod(name = "submitData", path = "sensor/submit", httpMethod = HttpMethod.POST)
	
	public Profile saveProfile(final User user, ProfileForm profileForm)
			throws UnauthorizedException {

		
	}
	
}
