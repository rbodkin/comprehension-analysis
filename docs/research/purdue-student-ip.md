# Purdue student IP: can a Purdue student contribute to this MIT-licensed repo?

Research for the licensing decision on `rbodkin/comprehension-analysis`. The repo is MIT-licensed and owned by Ron Bodkin, who is not at Purdue. A Purdue student will contribute code and research artifacts. Checked October 1, 2026 against Purdue's own pages. **This is not legal advice.** Claims marked **(inferred)** are my reading, not something Purdue states. Places where the policy is ambiguous are flagged **(ambiguous)**.

## Primary sources

| Short name | Source | Date |
|---|---|---|
| **I.A.1** | Purdue policy *Intellectual Property (I.A.1)*. <https://www.purdue.edu/vpec/policies/academic-research-affairs/ia1/> | Issued May 18, 2007; last revised April 28, 2025 |
| **Procedures** | *Procedures for Disclosure, Assignment and Commercialization of Intellectual Property* (these supplement I.A.1). <https://research.purdue.edu/resources-for-researchers/share-your-research/ip-procedures/> | Effective July 1, 2015 |
| **2013 Student Memo** | VP for Research R. Buckius memo, "Purdue Policy I.A.1 Concerning Ownership of University Course-Generated Intellectual Property Created by Students", with the attached signed clarification. <https://purdueinnovates.org/wp-content/uploads/2023/10/student-ip-ownership.pdf> | Feb 8, 2013 |
| **OTC Disclosure** | Purdue Innovates OTC page *Disclosure*, including the section "Interested in Releasing Software Under an Open Source License?". <https://purdueinnovates.org/otc/disclosure/> | Fetched 2026-10-01 |
| **OTC IP FAQ** | Purdue Innovates OTC page *Intellectual Property* (includes a "Student Intellectual Property (IP) Policy" section). <https://purdueinnovates.org/otc/intellectual-property/> | Fetched 2026-10-01 |
| **Outside Activity FAQ** | Office of Research, *Outside Activity and Intellectual Property FAQ*. <https://research.purdue.edu/resources-for-researchers/compliance-and-security/research-integrity/conflict-of-interest/ip-faq-outside-activity/> | Fetched 2026-10-01 |
| **Legacy OS form** | OTC *Request for Open Source Distribution* form and Certificate of Originality, 2009. It is still hosted, but it cites the superseded Executive Memorandum B-10. <https://purdueinnovates.org/wp-content/uploads/2023/10/disclosure_form_request_for_open_source_distribution_09_09_09_ae.doc> | Sept 2009 (historical) |
| **Thesis policy** | Graduate School, *Thesis and Dissertation Policies and Practices*. <https://www.purdue.edu/academics/ogsps/thesis/records-and-thesis-resources/thesis-and-dissertation-policies-and-practices/> | Fetched 2026-10-01 |
| **Grad Staff Manual** | *Graduate Staff Employment Manual* (copy hosted by the MSE department). <https://engineering.purdue.edu/MSE/academics/graduate/Graduate%20Staff%20Employment%20Manual> | May 2019 |
| **Sponsored Class Projects** | Office of Legal Counsel, *Sponsored Student Class Projects and Capstone Projects*. <https://www.purdue.edu/legalcounsel/resources/Projects.html> | Fetched 2026-10-01 |

Section numbering: the current I.A.1 page has no numbered sections, so I cite it by heading. The Procedures page renders as nested ordered lists and refers to its own "section III.D". That gives I = Custody and Disclosure, II = Assignment, III = Commercialization, IV = Advisory Committee. The sub-letters below follow that scheme **(inferred numbering)**.

## Answer in brief

- **Ownership turns on the student's role, not on how many Purdue resources they use.** I.A.1 claims all IP that "arises in any part in the course of employment or enrollment". There is no "significant use" test. "University Resource" is defined broadly, and "significant" is not defined anywhere in the current policy.
  - **Paid RA or employee**: Purdue owns. Works under a **sponsored project** follow the sponsor agreement.
  - **For course credit, unpaid, using only course-wide resources**: the student owns.
  - **Unpaid, not for credit, done on the student's own**: the policy has no explicit exception for students. This case is **(ambiguous)**.
- **Software exception.** I.A.1 lists contributions to open-source projects as an exception. The conditions: the funding sponsor and PI authorize it ("if any"), and any administrator directing the work consents. Code contributed to open source is also excluded from "Proprietary Software Code", which is the software category that must be disclosed.
- **Open-source release process.** OTC runs one: an "Open Source Request" disclosure, then a DocuSign *Open Source Release Request*. The final decision "rests with the Purdue Senior IP Officer in conjunction with the PRF Office of Technology Commercialization". OTC calls this "best practice". It publishes **no timeline**.
- **If Purdue owns the work, the student cannot personally assign it.** Procedures § II.B: "University personnel have no capacity or authority to assign or agree to assign Purdue Intellectual Property to a third party." So the student cannot sign an assignment-style CLA. I found no published Purdue position on CLAs.
- **Outside collaborators: keep the project outside Purdue.** If Ron joins a Purdue on-campus research project, Purdue would treat him as a visiting scientist and claim the IP he creates. The project should stay Ron's external project and not become a Purdue research project.

---

## 1. When does Purdue own a student's software or other copyrightable work?

### The general rule

I.A.1, "Statement of Policy", heading "Identification of Purdue Intellectual Property":

> "Intellectual Property that arises in any part in the course of employment or enrollment at the University, or in the course of a work-for-hire relationship or visiting scholar relationship with the University, is Purdue Intellectual Property, except as follows: …"

Students are bound by it. I.A.1, "Incorporation in Contracts and Permissions":

> "This policy is deemed 1) a term and condition of employment for every employee of the University, 2) a term and condition of enrollment and attendance at the University by students, and 3) a term and condition of permission to participate in any University research or other academic activity by any person (whether or not employed by, compensated by or enrolled at the University)."

Software is in scope. I.A.1, Definitions:

> "Copyrightable Work: An original work of authorship which has been fixed in any tangible medium of expression and is eligible for protection under the copyright laws of the United States. Software code is a Copyrightable Work."

"Intellectual Property" also covers "Research Data" and "Tangible Research Property". This matters for research artifacts such as datasets and labels. See [Research artifacts](#research-artifacts-data-papers-theses).

### The six exceptions (verbatim, I.A.1 "Identification of Purdue Intellectual Property")

1. "The University permits authors to retain and manage the copyright to Instructional Copyrightable Works and Scholarly Copyrightable Works, subject to a license in favor of the University as set forth below."
2. "The University permits a student to retain title to Intellectual Property that the student creates for credit and without compensation in a University course through the use of course-wide resources, provided that the Intellectual Property is not burdened by any pre-existing contractual obligation of the University."
3. "The University permits software code to be contributed to open-source projects upon (1) the authorization of the funding sponsor and principal investigator (if any) for the coding project and (2) the consent of the University administrator(s), if any, who request or direct the coding project."
4. "Intellectual Property from research directed and funded under a work-for-hire contract administered by the University's Sponsored Program Services is not Purdue Intellectual Property."
5. "Intellectual Property from research performed pursuant to a University contract that expressly exempts the research from the application of this policy is not Purdue Intellectual Property."
6. "Intellectual Property generated solely in the course of an Outside Activity without the use of University Resources or pre-existing Purdue Intellectual Property is not Purdue Intellectual Property."

Two relevant definitions (I.A.1, Definitions):

> "Scholarly Copyrightable Work: A Copyrightable Work created by any person subject to this policy primarily to express and preserve scholarship as evidence of academic advancement or academic accomplishment. Such works may include … works of students created in the course of their education, such as exams, projects, theses or dissertations, papers and articles."

> "Proprietary Software Code: A Copyrightable Work in the form of software code that is (a) either a Commissioned Copyrightable Work or authored in any part by University researchers with the aid of University Resources and (b) not contributed to an open-source coding project."

The Purdue license (I.A.1, "Purdue License to Scholarly Copyrightable Works…") reserves "a perpetual nonexclusive, royalty-free license … to use, duplicate and distribute the … Work for all research and educational purposes of the University." That license is non-exclusive, so it does not conflict with the work also being under MIT **(inferred)**.

### Scenario by scenario

**(a) Unpaid, not for credit (volunteer or side project)**

**(ambiguous)** The general rule claims IP arising "in any part in the course of … enrollment". The policy never defines that phrase for activity outside coursework and employment.

- The Outside Activity exception (#6) does not clearly apply. "Outside Activity" is defined as "Activity of a University employee that (a) occurs entirely outside of their University employment and entirely without use of University Resources and (b) is authorized in accordance with … (III.B.1)". That covers employees, not students as such.
- The policy's "Reason" section suggests that student IP is caught through use of Purdue resources: "…may result from the activities of University employees in the course of their employment or through the use, by University students or by any person, of University Resources."
- **(inferred)** If a student who is not employed by Purdue works on their own time, on their own hardware and accounts, with no Purdue funding, compute, lab, data or advisor direction, and the work is not part of their Purdue coursework or research, then the work has a good argument that it does not "arise in the course of enrollment". The policy does not say so explicitly.
- Exception #3 (open-source contribution) may independently cover the code. Its conditions are phrased "(if any)" and "if any". With no sponsor, no PI and no directing administrator, no authorizations are needed on the face of the text **(inferred)**. See §2 for the tension with OTC's guidance.
- The Outside Activity FAQ says OTC will issue a written ownership determination. That is the clean way to settle this case: "If OTC, in consultation with the Senior IP Officer, decides that either (i) the IP is not Purdue IP, or (ii) that the IP is not a candidate for commercialization, you will receive a written determination to that effect. Such a written determination can be useful when you are dealing with third parties…" The FAQ is written for employees. The OTC Disclosure page applies the disclosure route to anyone whose IP arises in "employment or enrollment".

**(b) For course credit (regular course)**

The student owns, under exception #2, if four conditions hold: the work is for credit, unpaid, uses only course-wide resources, and is free of pre-existing Purdue obligations. The 2013 Student Memo spells out the conditions:

> "(A) student innovator(s) made use of resources that are (i) routinely made available by the College/Department administering the University course; and (ii) are provided to all students enrolled in the course in an equitable manner; (B) the relevant student(s) are not paid by Purdue University, whether through internal funds or under a grant or contract with a third party; and (C) there are no preexisting obligations for Purdue in connection with such Course-Generated Intellectual Property."

For copyrightable works specifically, the memo's attached clarification, § A "Copyrightable Works", says:

> "As long as the only University resources used in the class project work for a University course are the general instructional laboratory facilities, equipment and resources that are made available by the College/Department and provided to all Purdue students enrolled for credit in the relevant Purdue course … and the University is not prohibited from doing so under relevant grants or contracts, then the University will consider such use of University resources by the Student(s) to be 'usually and customarily provided', and such copyrightable works generated by the Student(s) during the course will be Scholarly Copyrightable Work that will be owned by the relevant author(s) in accordance with applicable law."

Clarification § C requires re-disclosure if the student goes beyond course resources:

> "If that situation is not applicable to such premise, or the situation changes and the Student uses (or seeks to use) additional University resources beyond those usually and customarily provided by the College/Department to all students enrolled in the relevant course, then the matter should be fully disclosed at that time by the Faculty member responsible for the relevant course to the Department Head and the Office of Technology Commercialization (if necessary), in order to re-assess whether the University has any rights under applicable University policy."

The memo also says "The course syllabus is the ideal place to clarify student rights to ownership for the work performed in a course."

**(c) Independent study or research credit**

**(ambiguous)** Independent study is "for credit", but it often lacks "course-wide resources" in the memo's sense ("provided to all students enrolled in the course in an equitable manner"). It also usually involves a faculty supervisor's lab, compute or grant. Once resources beyond course-wide ones are used, memo § C sends the question back to OTC.

- The Scholarly Copyrightable Work exception (#1) explicitly lists "projects, theses or dissertations, papers and articles", so papers and writeups are the author's.
- Research software is less clear. If it is "authored in any part by University researchers with the aid of University Resources" and not contributed to open source, it is "Proprietary Software Code", which Purdue treats as disclosable Purdue IP (Procedures § I.B).
- **(inferred)** For independent-study code, the safe route is exception #3: contribute it to the open-source project with the supervising faculty member's sign-off as PI, or record in writing that there is no PI or sponsor.

**(d) Paid research assistant or other Purdue employee**

Purdue owns work in the scope of the job. It "arises … in the course of employment" (I.A.1 general rule). The Grad Staff Manual (May 2019, "Inventions, Patents, Copyrights, and Publishing") says:

> "The University owns all economic and property rights and the right to patent inventions and to copyright materials for all inventions and materials made or developed by University personnel either in the course of employment by the University or through the use of facilities or funds provided by or through the University. Graduate staff employment is subject to the University's policy on Intellectual Property (I.A.1)."

Being paid also defeats the course exception, whose condition (B) is "not paid by Purdue University, whether through internal funds or under a grant or contract with a third party". Employees must disclose and assign: Procedures § II.A requires that creators "execute a general assignment of title in favor of the University … In most instances the assignee will be Purdue Research Foundation."

**(inferred)** A paid RA who contributes to this repo entirely outside the RA job (unrelated topic, own time, own equipment) is in situation (a). For employees the Outside Activity exception does apply, but only if the activity is authorized under III.B.1 and uses no University Resources. The Outside Activity FAQ factors then apply: relation to scope of employment, use of pre-existing Purdue IP, help from Purdue personnel, and use of funds, facilities or equipment.

**(e) Under a sponsored research agreement**

The sponsor agreement controls.

- Procedures § I.A: "Purdue Intellectual Property that arises under third-party funding must be disclosed in accordance with the funding terms and these procedures."
- Exceptions #4 (work-for-hire contract administered by Sponsored Program Services) and #5 (a contract that "expressly exempts the research from the application of this policy") take the IP out of Purdue's hands entirely. In those cases the contract decides who owns it.
- Exception #3 needs "the authorization of the funding sponsor and principal investigator" before code is contributed to open source.
- The memo's condition (C) ("no preexisting obligations for Purdue") means sponsored work never qualifies for the student course exception.

**(f) "Significant" use of University resources: how Purdue defines it**

**It doesn't.** The current I.A.1 has no "significant use" threshold. Its only resource definition is broad:

> "University Resource: Any research support administered by or through Purdue University, including but not limited to funds, facilities, equipment or personnel."

The tests that appear in the policy are binary, or tied to a course:

- **Exception #6**: "without the use of University Resources". Any use counts.
- **Proprietary Software Code**: "with the aid of University Resources".
- **2013 memo**: resources "usually and customarily provided" to all students in the course.

Older language does use a threshold, but it is not current policy:

- The 2009 Legacy OS form warns that "if this Software is updated or otherwise further developed by any of the undersigned making significant use of Purdue-administered funds or facilities, Purdue may assert further rights."
- The OTC IP FAQ page summarizes a "Copyright Policy" under which rights stay with the creator unless, among other things, "The creator of the copyrightable work made more than incidental use of University resources." That list appears to describe pre-2007 policy (Executive Memorandum B-10, superseded by I.A.1 on May 18, 2007). I.A.1 itself has no "incidental" carve-out **(inferred; the OTC page is stale and should not be relied on over I.A.1)**.

**(inferred)** "Personnel" in the definition means a Purdue faculty member's supervision is itself a University Resource. Supervision by Ron, who is not at Purdue, is not.

### Research artifacts (data, papers, theses)

- **Papers and theses**: the author keeps copyright (exception #1). The Thesis policy says "Purdue University Policy I.A.1 … established that copyright ownership now resides with you, the author." It also grants Purdue a non-exclusive license to reproduce and distribute theses.
- **Research Data**: listed as Intellectual Property and defined as "The recorded factual material commonly accepted in the research and scholarly communities as necessary to validate research findings…". If it arises in Purdue research, Purdue owns it. The Outside Activity FAQ gives an example: lab-collected data used outside Purdue needs "a Data Use Agreement" via the Senior IP Officer. **(inferred)** Datasets, labels and annotations the student makes inside a Purdue research project should not go into this repo without that clearance. The same artifacts made under scenario (a) or (b) are not caught by this.

---

## 2. Purdue's process for open-source release

**The process (OTC Disclosure page, "Interested in Releasing Software Under an Open Source License?"):**

> "First, file a disclosure with OTC Invention Disclosure Portal. You will be contacted by OTC to review recommended licenses and discuss a strategy that meets the your goals."

> "Best practice before releasing software via an Open Source License:
> - File a disclosure with OTC Invention Disclosure Portal (… select 'Copyright' as Disclosure Type; type in Description field 'Open Source Request'; then complete only required fields …)
> - If you have already filed a disclosure with OTC and wish to request approval to release Open Source, contact your OTC Business Development Manager directly, or email otclicenses@prf.org.
> - You will be contacted by OTC to review recommended licenses and discuss a strategy that meets the team's goals
> - Following your discussion with OTC, if appropriate, you will receive a link to a DocuSign form (Purdue University Open Source Release Request) where you can provide more detailed information (such as whether or not third-party code is incorporated in your code, funding obligations that may prohibit open release, etc.) …
> - Ultimately, the decision whether to release code under an open source license rests with the Purdue Senior IP Officer in conjunction with the PRF Office of Technology Commercialization."

The page also warns that open source "sometimes results in inadvertent granting of patent rights that can affect the rights of authors and other researchers at the University". The MIT license has no express patent grant, though an implied license is arguable **(inferred)**.

**When is it required? (ambiguous)** The policy and OTC's guidance pull in different directions:

- **Policy text.** I.A.1 exception #3 permits contribution to open-source projects with only (1) sponsor and PI authorization "(if any)" and (2) the consent of a directing administrator "if any". It names no OTC approval. Procedures § I.B requires written disclosure of "an Invention, Proprietary Software Code or Commissioned Copyrightable Work", and code "contributed to an open-source coding project" is excluded from Proprietary Software Code by definition.
- **OTC guidance.** OTC presents the disclosure as "Best practice" and says the release decision "rests with the Purdue Senior IP Officer". The Disclosure page's general rule says disclosure is due "Whenever you have intellectual property (including software and source code) that arises in the course of your employment or enrollment at Purdue".
- **(inferred)** For Purdue-owned code, OTC approval is the safe course and arguably expected. It becomes essential when there is a sponsor, a PI, or a possible invention. For code the student owns (scenarios (a) or (b)), the release process is not triggered. In unclear cases, a written OTC determination settles it.

**How long it takes: not published.** I found no stated turnaround for open-source requests. The only published clocks are for other things:

- Procedures § III.A: "In most instances, the Supporting Organization will report the investment decision to the disclosing researchers within 180 days of receipt of the disclosure." This is for commercialization evaluation, not open-source requests.
- The Legal Counsel page on sponsored class projects: "We recommend allowing at least one month for processing."
- **(inferred)** Plan for weeks, not days, and ask OTC (otclicenses@prf.org, 765-588-3475) for an estimate.

**Historical license template.** The 2009 Legacy OS form proposed a standard license under "Copyright (c) <Year> <Purdue University> All rights reserved", an NCSA/BSD-style permissive text. It also said: "IF there are non-Purdue authors/creators, please contact our office for further direction." The current DocuSign form is not public, so I cannot confirm what it says today.

---

## 3. CLAs: can the student sign, or must Purdue?

**If Purdue owns the work, the student cannot assign it.** Procedures § II.B:

> "Assigning Purdue Intellectual Property to any third party other than a Supporting Organization is not permitted, unless specifically directed by the EVPRP or the Senior IP Officer. Except and unless as directed by the Senior IP Officer, University personnel have no capacity or authority to assign or agree to assign Purdue Intellectual Property to a third party."

- A copyright-assignment CLA from the student covering Purdue-owned code would be outside their authority. Only the Senior IP Officer (or the EVPRP) can direct it.
- **(inferred)** A license-style CLA, such as the Apache ICLA, is not literally an "assignment". But a non-owner cannot grant a valid copyright license to someone else's work. So for Purdue-owned code, any CLA would need to be signed or authorized by Purdue, through OTC or the Senior IP Officer, typically as a corporate or entity CLA.
- The superseded 2011 text of I.A.1 § VI said more broadly that "No creator of University Intellectual Property has the capability or authority to assign, license or otherwise dispose of University Intellectual Property except to the University or its designee." That language is not in the current policy.
- **(ambiguous)** The Procedures say "University personnel". Whether an unpaid student is "personnel" is not defined. Students are bound by the policy as a whole through "Incorporation in Contracts and Permissions".

**If the student owns the work, they can sign a CLA themselves.** This covers scenario (a) when it really is outside Purdue, the course exception, and Scholarly Copyrightable Works. The work stays subject only to Purdue's non-exclusive license over Scholarly Copyrightable Works, which is compatible with MIT **(inferred)**.

**Purdue's position on CLAs or outside contributions.** I found no published Purdue position on CLAs or on contributing to external open-source projects beyond I.A.1 exception #3 and the OTC open-source release process. Searches of purdue.edu, purdueinnovates.org and prf.org turned up nothing CLA-specific.

**Implication for this repo (inferred):**

- An **inbound=outbound** model (contributions under MIT, optionally with a DCO `Signed-off-by`) avoids asking the student to sign anything that assigns or relicenses. A DCO sign-off still certifies "I have the right to submit it". The student can only certify that truthfully if they own the code or Purdue has approved the release.
- An **assignment CLA** to Ron is the option most likely to collide with Procedures § II.B if Purdue has any claim.

---

## 4. Student collaborations with outside (non-Purdue) researchers

- **Don't let the outside researcher join a Purdue research project, unless that is intended.** Outside Activity FAQ: "A third party who participates directly in an on-campus research project is a visiting scientist, and therefore subject to Purdue's IP Policy, which provides that the resulting IP would be owned by Purdue." I.A.1 also binds "any person (whether or not employed by, compensated by or enrolled at the University)" as "a term and condition of permission to participate in any University research or other academic activity".
  - **(inferred)** If the collaboration is set up as a Purdue research project, for example under a Purdue faculty PI or as a lab project, Purdue could claim Ron's own contributions made within it.
  - Keeping `comprehension-analysis` as Ron's external project, to which the student contributes, avoids this.
- **Sponsored class or capstone projects.** If Ron proposes the work as a sponsored class project, the Office of Legal Counsel process applies: a Sponsor Acknowledgment Form and an Instructor Acknowledgment, "at least one month" to process, and "Purdue does not enter into contracts or NDAs with Sponsors. … Sponsors will receive the student project results." If pre-existing Purdue IP is involved, students must sign an acknowledgment. Under the 2013 memo, students in such courses keep ownership if the memo's conditions hold. Collaborating companies "may want written agreements transferring intellectual property ownership or license rights resulting from such course projects" (2013 memo).
- **Mixed authorship complicates a Purdue release.** The 2009 Legacy OS form flags non-Purdue authors as needing special handling ("contact our office for further direction"). Its Certificate of Originality asks how any third party "acquire[d] title".
- **Pre-existing Purdue IP.** Using Purdue code, data or tools in the outside project reintroduces Purdue rights in every scenario. Exception #6 and the FAQ both turn on "pre-existing Purdue Intellectual Property".
- **Prohibited transfers.** Since April 2025, I.A.1 "prohibits the transfer, license, or sublicense of Intellectual Property and Statutorily Restricted Research Results to a Prohibited Person". That means entities tied to a "foreign adversary" per 15 CFR 7.4. **(inferred)** It probably does not apply here. But a public MIT release of Purdue-owned code is a license to everyone, which is one more reason OTC wants to review releases of Purdue-owned code.

---

## Facts about the student's situation that decide the outcome

1. **Is the student paid by Purdue in any way** (RA, TA, hourly, fellowship paid through a grant)? If so, and the work relates to the job, Purdue owns it.
2. **Is the work for credit**, and in which kind of course? A regular course with course-wide resources favors the student. Independent study or thesis research is ambiguous.
3. **Is there external funding or a sponsor** behind the student's work or the supervising lab (grant, industry gift, sponsored agreement)? If so, the agreement governs, and exception #3 needs the sponsor's authorization.
4. **Which Purdue resources are used**: Purdue compute (RCAC, lab GPUs), Purdue-licensed API keys or software, Purdue datasets, lab space, or a Purdue faculty member's direction? Any use can bring the work under I.A.1. There is no "significant" threshold.
5. **Is there a Purdue PI or administrator directing the coding?** If so, their authorization and consent is what exception #3 requires.
6. **Does the contribution use pre-existing Purdue IP** (code, data, models from a Purdue lab)?
7. **Is the collaboration framed as Purdue research** (Ron as a visiting collaborator on a Purdue project), or as the student contributing to Ron's external project?
8. **Is the contribution software, or Research Data or other research artifacts?** Papers are the author's. Research data from Purdue research needs a data use agreement.
9. **Is there anything potentially patentable?** That brings in OTC's patent concerns and the public-disclosure timing on the OTC Disclosure page.

**Cleanest path (inferred):**

- If facts 1, 3, 4, 5 and 6 are all "no": the student likely owns their contributions and can contribute under MIT.
- Ideally, also get a short written OTC determination ("not Purdue IP" or "approved for open-source contribution"). That documents title for the repo.
- If any of those facts is "yes": have the student file an OTC "Open Source Request" disclosure naming MIT and this repo, with the PI's or sponsor's sign-off. Use inbound=outbound MIT plus DCO, not an assignment CLA.

## Open questions to put to Purdue

Contacts: OTC at otclicenses@prf.org; the Senior IP Officer (Associate VP, Sponsored Program Services) at 765-494-1063.

- Does Purdue treat unpaid, non-credit, off-resource student work as "arising in the course of enrollment"?
- Does I.A.1 exception #3 by itself (no sponsor, no PI) make contributed code not Purdue IP, or is OTC approval still required?
- What is the current turnaround for an Open Source Release Request?
- Will OTC sign or authorize a CLA or DCO for Purdue-owned contributions, and does it require the copyright line to read "Purdue University" (as the 2009 template did)?
