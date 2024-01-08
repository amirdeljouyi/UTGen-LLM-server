/*
 * Copyright 2012-2019 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.samples.petclinic.system;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.samples.petclinic.owner.Owner;
import org.springframework.samples.petclinic.owner.OwnerRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Controller
public class WelcomeController {

	private OwnerRepository owners;

	public WelcomeController() {
	}

	@GetMapping("/")
	public String welcome() {
		int pageSize = 5;
		int page = 1;
		String lastName = "Black";

//		Pageable pageable = PageRequest.of(page - 1, pageSize);
//		Page<Owner> ownersResults = owners.findAll();
//		ownersResults.getContent()
//		model.addAttribute("listOwners", ownersResults);
//		List<Owner> listOwners = owners.findAll(pageable);
//		model.addAttribute("listOwners", listOwners);

//		Optional<Owner> foundPerson = owners.findByLastName(lastName);
//		List<Owner> listOwners = new ArrayList<>();
//		if(foundPerson.isPresent())
//			listOwners.add(foundPerson.get());
//		model.addAttribute("listOwners", listOwners);


		return "welcome";
	}

	@GetMapping("/wowner")
	public Owner findOwner(@PathVariable(name = "ownerId", required = false) Integer ownerId) {
		return ownerId == null ? new Owner() : this.owners.findById(ownerId).get();
	}

}
