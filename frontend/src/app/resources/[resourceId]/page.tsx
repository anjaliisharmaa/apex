'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { 
  ArrowLeftIcon,
  BookmarkIcon,
  CalendarIcon,
  ClockIcon,
  UserIcon,
  StarIcon,
  EyeIcon,
  ShareIcon,
  PrinterIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface ResourceContent {
  id: string
  title: string
  summary: string
  content: string
  category: string
  type: 'policy' | 'guide' | 'story' | 'faq' | 'news'
  readTime: string
  publishDate: string
  lastUpdated: string
  author: string
  authorRole: string
  views: number
  rating: number
  tags: string[]
  relatedResources: string[]
  isFeatured?: boolean
}

// Detailed resource content
const resourcesContent: { [key: string]: ResourceContent } = {
  '1': {
    id: '1',
    title: 'POSH Act 2013: Complete Guide for Women Scientists',
    summary: 'Comprehensive guide covering all aspects of the Prevention of Sexual Harassment Act and your rights in the workplace.',
    category: 'legal',
    type: 'guide',
    readTime: '15 min read',
    publishDate: '2024-01-15',
    lastUpdated: '2024-02-15',
    author: 'Legal Team',
    authorRole: 'APEX Legal Department',
    views: 1247,
    rating: 4.8,
    tags: ['POSH Act', 'Workplace Rights', 'Sexual Harassment', 'Legal Protection'],
    relatedResources: ['2', '4', '5'],
    isFeatured: true,
    content: `
# Prevention of Sexual Harassment Act 2013: Complete Guide

## Introduction

The Prevention of Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 is a landmark legislation that provides protection against sexual harassment of women at workplace and ensures a safe and secure working environment for all.

## Key Provisions of the Act

### Definition of Sexual Harassment

Sexual harassment includes any one or more of the following unwelcome acts or behaviour:
- Physical contact and advances
- A demand or request for sexual favours
- Making sexually coloured remarks
- Showing pornography
- Any other unwelcome physical, verbal or non-verbal conduct of sexual nature

### Workplace Coverage

The Act covers:
- All government and private organizations
- Educational institutions
- Sports institutions
- Any place visited by employees arising out of employment

## Rights Under POSH Act

### Right to Complaint
- Every woman has the right to file a complaint of sexual harassment
- Complaints can be filed with the Internal Complaints Committee (ICC)
- For external complainants, complaints can be filed with Local Complaints Committee (LCC)

### Right to Safe Work Environment
- Employers must provide a safe working environment
- Prevention of sexual harassment through awareness programs
- Regular sensitization programs for employees

### Right to Confidentiality
- Identity of complainant and respondent to be kept confidential
- No publication of details of sexual harassment proceedings

## Internal Complaints Committee (ICC)

### Composition
- Presiding Officer: Senior woman employee
- Two employees from amongst employees
- One external member from NGO or person familiar with issues related to sexual harassment

### Functions
- Receive and investigate complaints
- Conduct inquiry in prescribed manner
- Submit report with recommendations
- Ensure compliance with recommendations

## Complaint Process

### Step 1: Filing Complaint
- Written complaint to be filed within 3 months of incident
- Extension up to 3 more months with valid reasons
- Complaint can be filed by affected woman or any person on her behalf

### Step 2: Investigation
- ICC to conduct inquiry within 90 days
- Opportunity to both parties to be heard
- Cross-examination of witnesses
- Recording of evidence

### Step 3: Resolution
- Conciliation if requested by complainant
- Final report with findings and recommendations
- Action to be taken within 60 days

## Penalties and Consequences

### For Organizations
- Failure to constitute ICC: Rs. 50,000 fine
- Non-compliance with Act provisions: Rs. 50,000 fine
- Repeated violations: Higher penalties and cancellation of license

### For Individuals
- Disciplinary action including termination
- Deduction from salary for compensation
- Counseling and awareness programs

## Recent Updates and Amendments

### 2024 Guidelines
- Enhanced digital workplace protections
- Remote work harassment provisions
- Social media harassment inclusion
- Revised penalty structures

### Technology Integration
- Online complaint filing systems
- Digital awareness modules
- Virtual ICC proceedings
- Electronic evidence handling

## Best Practices for Organizations

### Prevention Strategies
- Regular awareness workshops
- Clear communication of policies
- Accessible complaint mechanisms
- Regular training for ICC members

### Response Protocols
- Prompt acknowledgment of complaints
- Fair and impartial investigation
- Appropriate remedial action
- Follow-up monitoring

## Support Resources

### Internal Support
- ICC contact details
- Employee assistance programs
- Counseling services
- Legal aid assistance

### External Support
- National Commission for Women
- State Women Commission
- NGO partners
- Legal aid clinics

## Frequently Asked Questions

### Q: Can men file complaints under POSH Act?
A: The Act specifically covers sexual harassment of women. However, organizations should have separate policies for all employees.

### Q: What if the harasser is a client or customer?
A: The Act covers harassment by third parties, and employers are liable to provide protection.

### Q: Is emotional harassment covered?
A: Yes, unwelcome verbal conduct of sexual nature is covered under the Act.

### Q: Can complaints be filed anonymously?
A: While anonymous complaints can be received, investigation requires identity disclosure for fair proceedings.

## Conclusion

The POSH Act 2013 is a crucial legal framework that ensures workplace dignity and safety for women. Understanding your rights and the complaint process empowers you to take action against sexual harassment and contributes to creating a safer work environment for all.

Remember: Every woman deserves a workplace free from harassment, and it is both a legal right and moral imperative to ensure this protection.

---

*This guide is for informational purposes. For specific legal advice, consult with qualified legal professionals.*
    `
  },
  '2': {
    id: '2',
    title: 'Maternity Benefits Act: Everything You Need to Know',
    summary: 'Detailed explanation of maternity benefits, leave entitlements, and how to apply for various benefits.',
    category: 'policies',
    type: 'policy',
    readTime: '12 min read',
    publishDate: '2024-01-20',
    lastUpdated: '2024-02-20',
    author: 'HR Department',
    authorRole: 'Human Resources Team',
    views: 892,
    rating: 4.7,
    tags: ['Maternity Benefits', 'Leave Policy', 'Women Rights', 'Healthcare'],
    relatedResources: ['1', '4', '6'],
    isFeatured: true,
    content: `
# Maternity Benefits Act 2017: Complete Guide

## Overview

The Maternity Benefit Act, 2017 is a significant legislation that enhances the rights of working women by providing better maternity benefits and ensuring job security during pregnancy and childbirth.

## Key Benefits Under the Act

### Maternity Leave
- **26 weeks paid maternity leave** for first two children
- **12 weeks paid maternity leave** for more than two children
- Leave can be taken from 8 weeks before expected delivery date
- Maximum 8 weeks before delivery, minimum 6 weeks after delivery

### Adopting Mother Benefits
- **12 weeks maternity benefit** for adopting mothers
- Available for children below 3 months of age
- Same salary and benefits as biological mothers

### Commissioning Mother Benefits
- **12 weeks maternity benefit** for commissioning mothers (surrogacy)
- From the date child is handed over
- Applicable for genetic mother in surrogacy arrangements

## Eligibility Criteria

### Employment Requirements
- Employed for at least 80 days in 12 months preceding expected delivery date
- Regular employee with continuous service
- Part-time and contractual employees covered

### Documentation Required
- Medical certificate confirming pregnancy
- Expected date of delivery
- Employment proof and service records
- Application form as prescribed

## Application Process

### Step 1: Notification
- Inform employer at least 6 weeks before availing leave
- Submit medical certificate with expected delivery date
- Provide required documentation

### Step 2: Application Submission
- Fill prescribed application form
- Attach all supporting documents
- Submit to HR department or designated authority

### Step 3: Approval and Processing
- Employer to acknowledge application
- Verification of eligibility criteria
- Approval notification with leave period details

## Salary and Benefits During Leave

### Payment Structure
- Full salary during entire leave period
- All applicable allowances and benefits
- No deduction for maternity leave period
- Timely payment as per regular schedule

### Additional Benefits
- Medical expenses reimbursement
- Nursing break entitlements
- Job protection and security
- Increments and promotions not affected

## Work From Home Provisions

### Post-Delivery Work Arrangements
- Option to work from home after exhausting maternity leave
- Negotiable based on nature of work
- Mutual agreement between employer and employee
- Facility for up to 6 months

### Nursing Break
- Two nursing breaks daily until child is 15 months old
- Each break of at least 30 minutes duration
- Breaks counted as working hours
- Flexible timing arrangements

## Employer Obligations

### Mandatory Provisions
- Provide maternity benefits as per Act
- Ensure job security during pregnancy and leave
- Maintain position and pay scales
- Create supportive work environment

### Crèche Facilities
- Establishments with 50+ women employees must provide crèche
- Allow 4 visits per day to crèche during working hours
- Safe and hygienic childcare facilities
- Qualified staff for child supervision

### Awareness and Training
- Educate employees about maternity rights
- Train supervisors on supportive practices
- Display information about benefits prominently
- Regular policy updates and communications

## Recent Enhancements (2024)

### Extended Benefits
- Enhanced medical coverage during pregnancy
- Paternity leave provisions for fathers
- Adoption benefits improved
- Miscarriage leave entitlements

### Digital Services
- Online application systems
- Digital tracking of applications
- E-certificates and approvals
- Mobile apps for benefit tracking

## Common Scenarios and Solutions

### Premature Delivery
- Leave entitlement remains same (26/12 weeks)
- Additional medical support if required
- Flexible return-to-work options
- Extended nursing break provisions

### Multiple Pregnancies
- Same leave entitlement per pregnancy
- Additional medical care coverage
- Special considerations for twins/multiples
- Enhanced childcare support

### Miscarriage or Medical Termination
- 6 weeks paid leave for miscarriage after 20 weeks
- Medical support and counseling
- No impact on future maternity benefits
- Confidential handling of cases

## Support Systems

### Healthcare Support
- Regular health check-ups
- Maternity insurance coverage
- Emergency medical assistance
- Specialized medical consultations

### Counseling Services
- Pre and post-natal counseling
- Career planning support
- Mental health assistance
- Peer support groups

### Legal Assistance
- Guidance on rights and entitlements
- Complaint resolution mechanisms
- Legal aid for violations
- Advocacy support services

## Penalties for Non-Compliance

### Employer Violations
- Fine up to Rs. 20,000 for non-payment
- Imprisonment up to 1 year for repeated violations
- Compensation to affected employees
- Legal action for discrimination

### Enforcement Mechanisms
- Labor department inspections
- Employee complaint systems
- NGO advocacy and support
- Court interventions when required

## Global Comparisons

### International Standards
- India's 26 weeks among highest globally
- Comparison with other developing nations
- WHO recommendations compliance
- ILO convention adherence

## Future Developments

### Proposed Enhancements
- Extended leave duration discussions
- Enhanced adoption benefits
- Digital infrastructure improvements
- Inclusive policy expansions

## Important Contacts

### Government Agencies
- Ministry of Labour and Employment
- State Labour Departments
- Women and Child Development Ministry
- National Commission for Women

### Support Organizations
- Women's rights NGOs
- Legal aid societies
- Employee unions
- Professional associations

## Conclusion

The Maternity Benefits Act 2017 represents a significant step forward in supporting working mothers and ensuring gender equality in the workplace. Understanding these benefits empowers women to make informed decisions about their careers and families.

---

*For specific queries about your entitlements, consult with your HR department or legal advisor.*
    `
  },
  '3': {
    id: '3',
    title: 'Dr. Sunita Sharma: Breaking Barriers in DRDO',
    summary: 'Inspiring journey of Dr. Sunita Sharma who became the first woman scientist to lead a major defense project.',
    category: 'stories',
    type: 'story',
    readTime: '8 min read',
    publishDate: '2024-02-01',
    lastUpdated: '2024-02-01',
    author: 'Editorial Team',
    authorRole: 'APEX Editorial',
    views: 654,
    rating: 4.9,
    tags: ['Success Story', 'Women in Science', 'DRDO', 'Leadership', 'Inspiration'],
    relatedResources: ['6', '4', '5'],
    isFeatured: true,
    content: `
# Dr. Sunita Sharma: Breaking Barriers in DRDO

## The Beginning of an Extraordinary Journey

Dr. Sunita Sharma's story is one of determination, brilliance, and breaking through the glass ceiling in one of India's most prestigious scientific organizations - the Defence Research and Development Organisation (DRDO). Her journey from a small town in Rajasthan to becoming the first woman scientist to lead a major defense project is nothing short of inspiring.

## Early Life and Education

### Humble Beginnings
Born in 1978 in a small town near Jodhpur, Rajasthan, Sunita was the daughter of a school teacher and a homemaker. From an early age, she showed exceptional aptitude in mathematics and science, often outperforming her peers in academic competitions.

### Academic Excellence
- **B.Tech in Electronics Engineering** from IIT Delhi (1999)
- **M.Tech in Signal Processing** from IIT Delhi (2001)
- **Ph.D in Advanced Radar Systems** from IIT Delhi (2005)

Her doctoral thesis on "Adaptive Signal Processing for Multi-Target Tracking Systems" received the Best Thesis Award and was later published in several international journals.

## Career Journey at DRDO

### Early Years (2005-2010)
Dr. Sharma joined DRDO's Electronic & Radar Development Establishment (LRDE) in Bangalore as a Scientist 'B' in 2005. Her initial years were spent working on:

- **Radar Signal Processing Systems**
- **Electronic Warfare Technologies**
- **Surveillance and Reconnaissance Systems**

Despite being one of the few women in her team, she quickly established herself as a brilliant researcher and innovator.

### Rising Through the Ranks (2010-2015)
Her breakthrough came with the development of an advanced multi-mode radar system that significantly enhanced India's border surveillance capabilities. This work earned her:

- **Young Scientist Award** (2012)
- **Technology Group Award** for Innovation (2013)
- **Promotion to Scientist 'E'** (2014)

### Leadership Challenges
As she progressed in her career, Dr. Sharma faced unique challenges:

#### Gender Bias
- Being questioned about her technical capabilities
- Exclusion from certain "boys club" meetings
- Balancing family responsibilities with demanding project schedules

#### Professional Obstacles
- Limited representation of women in senior positions
- Stereotypes about women in defense technology
- Pressure to prove herself repeatedly

### The Breakthrough Project (2016-2020)

#### Project AAKASH: Next-Generation Air Defense System
In 2016, Dr. Sharma was selected to lead Project AAKASH, a critical air defense initiative worth ₹500 crores. This made her the first woman scientist to head a major defense project in DRDO's history.

**Project Scope:**
- Development of indigenous air defense radar system
- Integration with missile guidance systems
- Real-time threat assessment and response
- Multi-platform compatibility

**Challenges Faced:**
- Managing a team of 150+ scientists and engineers
- Coordinating with international technology partners
- Meeting strict defense ministry deadlines
- Ensuring highest security protocols

### Innovation and Leadership Style

#### Technical Innovations
Under Dr. Sharma's leadership, Project AAKASH achieved several technological breakthroughs:

1. **Advanced Signal Processing Algorithms**
   - 40% improvement in target detection accuracy
   - Reduced false alarm rates by 60%
   - Enhanced performance in adverse weather conditions

2. **Artificial Intelligence Integration**
   - Machine learning for threat classification
   - Predictive maintenance systems
   - Automated response protocols

3. **Cost Optimization**
   - 30% reduction in manufacturing costs
   - Indigenous component development
   - Scalable production models

#### Leadership Philosophy
Dr. Sharma's approach to leadership emphasizes:

- **Collaborative Decision Making:** Involving team members in critical decisions
- **Mentorship:** Actively mentoring young scientists, especially women
- **Innovation Culture:** Encouraging creative thinking and risk-taking
- **Work-Life Balance:** Understanding personal commitments of team members

## Personal Life and Challenges

### Balancing Act
Throughout her career, Dr. Sharma has successfully balanced her professional achievements with personal responsibilities:

- **Marriage in 2008** to Dr. Rajesh Kumar, also a DRDO scientist
- **Motherhood in 2012** - daughter Ananya
- **Continued career growth** without compromising family time

### Support Systems
She credits her success to strong support systems:

- **Family Support:** Husband and in-laws who shared domestic responsibilities
- **Professional Mentors:** Senior scientists who guided her career
- **Peer Networks:** Women scientists' associations and support groups
- **Organizational Policies:** DRDO's progressive policies for women employees

## Recognition and Awards

### National Recognition
- **Shanti Swarup Bhatnagar Prize** for Engineering Sciences (2019)
- **Padma Shri** for contributions to science and technology (2021)
- **DRDO Performance Excellence Award** (2020)
- **Women Scientist Award** by Department of Science & Technology (2018)

### International Acclaim
- **IEEE Fellow** for contributions to radar technology (2020)
- **International Women in Engineering Award** (2021)
- **Featured in MIT Technology Review's Innovators Under 45** (2019)

## Current Role and Future Vision

### Present Position
Dr. Sharma currently serves as **Director, Advanced Defense Technologies** at DRDO headquarters in New Delhi, where she oversees multiple critical projects and strategic initiatives.

### Future Goals
Her vision for the future includes:

1. **Increasing Women's Participation** in defense research
2. **Technology Transfer** to private industry
3. **International Collaborations** in defense technology
4. **Startup Ecosystem** for defense innovations

### Mentorship Initiatives
She has launched several programs to support women in science:

- **DRDO Women Scientists Network**
- **Young Innovators Program**
- **School Outreach Initiatives**
- **Scholarship Programs** for girl students in engineering

## Impact on Organization Culture

### Policy Changes
Dr. Sharma's success has led to several organizational improvements:

- **Flexible Working Hours** for parents
- **On-site Childcare Facilities**
- **Enhanced Maternity Benefits**
- **Women's Safety Committees**

### Inspiring the Next Generation
Her journey has inspired many young women to pursue careers in defense research:

- **50% increase** in women applicants to DRDO
- **More women** in leadership positions
- **Improved retention rates** among women scientists
- **Cultural shift** towards gender inclusivity

## Lessons from Her Journey

### Key Takeaways
1. **Technical Excellence** is the foundation of success
2. **Persistence** in face of challenges pays off
3. **Mentorship** and support networks are crucial
4. **Work-life balance** is achievable with proper planning
5. **Breaking barriers** requires courage and determination

### Advice for Aspiring Women Scientists
Dr. Sharma's message to young women entering science careers:

> "Don't let anyone tell you that defense technology is not for women. We bring unique perspectives, analytical thinking, and collaborative approaches that strengthen our scientific capabilities. Believe in yourself, stay curious, and never stop learning."

## Future of Women in Defense Research

### Growing Opportunities
The success of scientists like Dr. Sharma is opening new avenues:

- **Increased representation** in senior positions
- **Policy reforms** supporting women professionals
- **Cultural changes** in traditionally male-dominated fields
- **International recognition** of Indian women scientists

### Continuing Challenges
Despite progress, challenges remain:

- **Work-life balance** pressures
- **Gender stereotypes** in technical fields
- **Limited role models** in certain specializations
- **Institutional biases** that need addressing

## Conclusion

Dr. Sunita Sharma's journey from a small town in Rajasthan to leading one of India's most critical defense projects exemplifies what's possible when talent meets opportunity and determination. Her story is not just about personal success but about changing an entire organizational culture and inspiring a generation of women scientists.

Her legacy lies not only in the technological innovations she has contributed but also in the barriers she has broken and the path she has paved for others to follow. As she continues to lead and innovate, Dr. Sharma remains a beacon of hope and inspiration for women in science across India and beyond.

### Recognition Quote
*"Dr. Sunita Sharma represents the best of Indian scientific talent. Her contributions to defense technology and her role in promoting gender equality in STEM make her a true national asset."* - Dr. G. Satheesh Reddy, Former Chairman, DRDO

---

*This story is part of our ongoing series celebrating women leaders in Indian science and technology.*
    `
  },
  '4': {
    id: '4',
    title: 'Child Care Leave: Updated Guidelines 2024',
    summary: 'New guidelines for child care leave including extended provisions and simplified application process.',
    category: 'policies',
    type: 'policy',
    readTime: '10 min read',
    publishDate: '2024-02-10',
    lastUpdated: '2024-02-10',
    author: 'Policy Team',
    authorRole: 'APEX Policy Department',
    views: 543,
    rating: 4.6,
    tags: ['Child Care', 'Leave Policy', 'Parenting', 'Work-Life Balance'],
    relatedResources: ['2', '1', '5'],
    content: `
# Child Care Leave: Updated Guidelines 2024

## Introduction

The updated Child Care Leave policy for 2024 introduces significant enhancements to support employees in balancing their professional responsibilities with child care needs. These guidelines reflect our commitment to creating a family-friendly workplace that recognizes the importance of child care in employee well-being and productivity.

## Eligibility and Scope

### Who Can Apply
- All permanent employees (both male and female)
- Contractual employees with minimum 2 years of service
- Probationary employees after confirmation
- Part-time employees (pro-rata benefits)

### Child Age Criteria
- Children up to 18 years of age
- Specially-abled children up to 22 years of age
- Adopted children from date of legal adoption
- Foster children with proper documentation

## Types of Child Care Leave

### 1. Regular Child Care Leave
- **Duration:** Up to 2 years during entire service
- **Age Limit:** Child must be under 18 years
- **Salary:** First 365 days at 100% salary, remaining period without pay
- **Benefits:** Medical coverage continues throughout

### 2. Extended Child Care Leave
- **Duration:** Additional 1 year (total 3 years)
- **Conditions:** Available for specially-abled children
- **Salary:** Without pay after first year
- **Support:** Special allowances may apply

### 3. Emergency Child Care Leave
- **Duration:** Up to 15 days per year
- **Purpose:** Sudden illness or emergency care needs
- **Salary:** Full pay
- **Documentation:** Medical certificate required for illness

### 4. Short-term Child Care Leave
- **Duration:** Up to 30 days per year
- **Purpose:** School events, medical appointments, examinations
- **Salary:** Full pay
- **Advance Notice:** Minimum 7 days (except emergencies)

## Application Process

### Step 1: Preparation
- Determine type and duration of leave required
- Gather necessary supporting documents
- Plan work handover and coverage arrangements
- Consult with immediate supervisor

### Step 2: Documentation Required
- **Application Form CCL-2024** (available on employee portal)
- **Child's birth certificate** or adoption papers
- **Medical certificate** (if applicable)
- **School enrollment certificate** (for school-age children)
- **Work handover plan**
- **Supervisor's recommendation**

### Step 3: Submission Timeline
- **Regular/Extended Leave:** 30 days advance notice
- **Emergency Leave:** Within 24 hours of emergency
- **Short-term Leave:** 7 days advance notice
- **Medical Emergency:** Immediate notification, documentation within 48 hours

### Step 4: Approval Process
1. Immediate supervisor review and recommendation
2. HR department verification and compliance check
3. Department head approval for leaves >30 days
4. Final approval notification within 7 working days

## Enhanced Benefits 2024

### Financial Support
- **Child Care Allowance:** ₹2,000 per month during leave period
- **Medical Insurance:** Continued coverage for child
- **Educational Assistance:** Up to ₹50,000 per year for specially-abled children
- **Emergency Fund:** Up to ₹25,000 for unexpected medical expenses

### Flexible Work Arrangements
- **Work from Home:** Up to 3 days per week post-leave
- **Flexible Hours:** Modified work schedules to accommodate child care
- **Part-time Options:** Reduced hours with proportional salary
- **Job Sharing:** Arrangements with other employees

### Wellness Support
- **Counseling Services:** Professional support for parenting challenges
- **Pediatric Consultations:** On-campus medical support
- **Nutrition Programs:** Guidance for child nutrition and health
- **Parenting Workshops:** Monthly educational sessions

## Special Provisions

### Specially-Abled Children
- **Extended Leave:** Up to 3 years total
- **Therapy Support:** Reimbursement for specialized treatments
- **Equipment Assistance:** Financial support for assistive devices
- **Caregiver Training:** Professional training for family members

### Adoption Cases
- **Immediate Leave:** From date of legal custody
- **Bonding Period:** Additional 30 days for family adjustment
- **Legal Support:** Assistance with adoption procedures
- **Counseling:** Pre and post-adoption family counseling

### Single Parents
- **Priority Processing:** Expedited approval for emergency leave
- **Extended Support:** Additional financial assistance
- **Flexible Return:** Gradual work reintegration options
- **Emergency Contacts:** 24/7 support for urgent situations

## Return to Work

### Reintegration Process
- **Advance Notice:** 30 days notice before returning
- **Skill Updates:** Training programs if required
- **Gradual Return:** Phased return to full responsibilities
- **Performance Support:** Additional mentoring if needed

### Position Protection
- **Same Level:** Return to equivalent position and pay grade
- **Promotion Eligibility:** Leave period counts for promotion consideration
- **Increment Protection:** Regular increments not affected
- **Benefits Restoration:** Full restoration of all employment benefits

### Continued Support
- **Follow-up Meetings:** Regular check-ins for first 3 months
- **Flexible Arrangements:** Ongoing work-life balance support
- **Career Counseling:** Guidance for career development post-leave
- **Peer Support:** Connection with other returning parents

## Employer Support Systems

### On-site Facilities
- **Crèche Services:** Professional childcare for children 6 months - 6 years
- **Lactation Rooms:** Private, comfortable nursing facilities
- **Play Areas:** Safe recreational spaces for children
- **Emergency Care:** Backup childcare for unexpected situations

### Technology Support
- **Remote Access:** Secure systems for work-from-home arrangements
- **Communication Tools:** Video conferencing for flexible participation
- **Mobile Apps:** Leave tracking and communication platforms
- **Digital Resources:** Online parenting resources and support

### Policy Integration
- **Leave Coordination:** Integration with other leave policies
- **Career Planning:** Alignment with professional development programs
- **Performance Management:** Adjusted metrics during transition periods
- **Succession Planning:** Coverage arrangements during extended leaves

## Compliance and Monitoring

### Legal Framework
- **Maternity Benefit Act 2017** compliance
- **Equal Employment Opportunity** adherence
- **State Labor Laws** integration
- **International Standards** alignment

### Quality Assurance
- **Regular Policy Reviews:** Annual updates based on feedback
- **Employee Surveys:** Satisfaction and improvement suggestions
- **Best Practice Research:** Industry benchmarking
- **Expert Consultations:** Child welfare and HR specialists

### Grievance Redressal
- **Open Door Policy:** Direct access to HR leadership
- **Anonymous Feedback:** Confidential reporting mechanisms
- **Ombudsman Service:** Independent review of concerns
- **Legal Support:** Assistance for policy violations

## Success Stories

### Case Study 1: Dr. Priya Mehta
Senior Research Scientist who successfully balanced a critical project delivery with caring for her specially-abled child using the extended child care leave provisions.

### Case Study 2: Mr. Rajesh Kumar
Single father who utilized emergency child care leave and flexible work arrangements to manage his child's sudden illness while maintaining project commitments.

### Case Study 3: Ms. Anitha Reddy
New adoptive parent who benefited from immediate leave provisions and counseling support during the family adjustment period.

## Future Enhancements

### Planned Improvements
- **Digital Integration:** AI-powered leave planning tools
- **Expanded Coverage:** Coverage for grandchildren in special circumstances
- **International Standards:** Alignment with global best practices
- **Community Partnerships:** Collaborations with childcare providers

### Research Initiatives
- **Impact Studies:** Long-term effects on employee satisfaction and retention
- **Best Practices:** Documentation and sharing of successful implementations
- **Technology Integration:** Innovative solutions for work-life balance
- **Policy Evolution:** Continuous improvement based on changing needs

## Important Contacts

### HR Support
- **Child Care Leave Coordinator:** ccl-support@apex.gov.in
- **Employee Helpline:** 1800-XXX-XXXX
- **24/7 Emergency Support:** emergency@apex.gov.in
- **Counseling Services:** counseling@apex.gov.in

### External Resources
- **Child Welfare Department:** State government resources
- **Medical Emergency Services:** Partner hospitals and clinics
- **Legal Aid:** Family law specialists
- **Community Support:** Local parent groups and NGOs

## Conclusion

The 2024 Child Care Leave guidelines represent our organization's commitment to supporting employees in their dual roles as professionals and parents. By providing comprehensive support, flexible arrangements, and enhanced benefits, we aim to create an environment where employees can thrive both personally and professionally.

These guidelines are designed to evolve with changing needs and circumstances. We encourage feedback and suggestions to continuously improve our support for working parents.

---

*For specific questions about your situation, please contact the Child Care Leave Coordinator or your HR representative.*
    `
  },
  '5': {
    id: '5',
    title: 'Frequently Asked Questions: Transfer Policies',
    summary: 'Common questions and answers about transfer policies, spouse grounds, and application procedures.',
    category: 'faq',
    type: 'faq',
    readTime: '6 min read',
    publishDate: '2024-02-15',
    lastUpdated: '2024-02-15',
    author: 'HR Department',
    authorRole: 'Human Resources Team',
    views: 432,
    rating: 4.5,
    tags: ['Transfer Policy', 'FAQs', 'Spouse Transfer', 'Career Mobility'],
    relatedResources: ['1', '2', '4'],
    content: `
# Frequently Asked Questions: Transfer Policies

## General Transfer Questions

### Q1: What are the different types of transfers available?
**A:** There are several types of transfers:
- **Administrative Transfer:** For organizational requirements
- **Mutual Transfer:** Exchange between two employees
- **Medical Transfer:** Due to health conditions
- **Spouse Ground Transfer:** For family reunification
- **Promotional Transfer:** Accompanying career advancement
- **Disciplinary Transfer:** For administrative reasons

### Q2: How often can I apply for a transfer?
**A:** You can apply for transfer once every year, except in emergency situations like medical grounds or spouse transfers where applications can be submitted as needed.

### Q3: What is the minimum service period required before applying for transfer?
**A:** Generally, you must complete at least 2 years of service at your current location before applying for transfer, except for spouse ground transfers and medical emergencies.

## Spouse Ground Transfer

### Q4: What documents are required for spouse ground transfer?
**A:** Required documents include:
- Spouse's employment certificate/offer letter
- Marriage certificate
- No objection certificate from current department
- Performance appraisal reports (last 2 years)
- Medical certificate (if spouse is posted due to medical reasons)

### Q5: How is spouse ground transfer different from regular transfer?
**A:** Spouse ground transfers:
- Have relaxed service period requirements
- Get priority consideration
- Don't count towards annual transfer quota
- Require supporting documentation about spouse's posting
- May have expedited processing

### Q6: Can unmarried employees apply for family ground transfer?
**A:** Yes, unmarried employees can apply for transfer on family grounds in cases of:
- Caring for elderly or sick parents
- Supporting specially-abled family members
- Being the only earning member responsible for family

### Q7: What if my spouse works in a private company?
**A:** Spouse ground transfer is valid even if your spouse works in private sector, provided:
- The employment is confirmed/permanent
- Employer provides official documentation
- The transfer is for business requirements, not personal choice

## Medical Ground Transfer

### Q8: What medical conditions qualify for transfer?
**A:** Qualifying conditions include:
- Chronic illnesses requiring specific climate/environment
- Need for specialized medical treatment available at specific locations
- Doctor's recommendation for health reasons
- Family member's medical condition requiring care

### Q9: How long does medical ground transfer take?
**A:** Medical ground transfers are given priority and typically processed within:
- Emergency cases: 15-30 days
- Regular medical grounds: 45-60 days
- Subject to position availability at requested location

## Application Process

### Q10: Where do I submit my transfer application?
**A:** Submit applications to:
1. Your immediate supervisor (for initial review)
2. Departmental transfer committee
3. HR transfer section
4. Copy to establishment section

### Q11: When is the best time to apply for transfer?
**A:** The optimal time varies by transfer type:
- **Regular transfers:** April-May (for July transfers)
- **Spouse ground:** Anytime when spouse gets posting order
- **Medical ground:** As soon as medical need arises
- **Administrative:** Based on organizational requirements

### Q12: Can I specify multiple preferred locations?
**A:** Yes, you can list up to 5 preferred locations in order of preference. This increases your chances of accommodation and helps in planning.

## Selection and Processing

### Q13: How are transfer requests prioritized?
**A:** Priority order typically follows:
1. Administrative requirements
2. Medical ground transfers
3. Spouse ground transfers
4. Mutual transfers
5. Regular voluntary transfers
6. Compassionate grounds

### Q14: What happens if my transfer is rejected?
**A:** In case of rejection:
- You receive written reasons for rejection
- Can reapply in next cycle unless specifically barred
- May appeal to higher authority within 30 days
- Can seek transfer committee review

### Q15: Can I withdraw my transfer application?
**A:** Yes, you can withdraw your application:
- Before final approval: Simple written request
- After approval but before joining: May require administrative approval
- After joining: Not applicable as transfer is completed

## Location and Posting

### Q16: Can I refuse a transfer order once issued?
**A:** Generally, transfer orders are binding, but you may request reconsideration in cases of:
- Extreme personal hardship
- Medical reasons
- Family emergencies
- Administrative errors in posting

### Q17: What if there's no vacancy at my preferred location?
**A:** Options include:
- Waiting for next transfer cycle
- Accepting alternative location offer
- Opting for temporary attachment
- Seeking mutual transfer arrangement

### Q18: Are there any locations with restrictions?
**A:** Yes, some restrictions apply:
- Field/remote postings may have tenure requirements
- Border areas may have security clearance needs
- Specialized units may require additional qualifications
- Some locations may have gender-specific considerations

## Benefits and Entitlements

### Q19: What are my entitlements during transfer?
**A:** Transfer entitlements include:
- Travel allowance for self and family
- Transportation of household goods
- Temporary accommodation allowance
- Leave travel concession
- Joining time as per rules

### Q20: How is my pay and allowances affected?
**A:** Generally:
- Basic pay remains unchanged
- Local allowances change based on new location
- Special allowances based on new posting type
- Dearness allowance as per new location classification

### Q21: What about children's education during transfer?
**A:** Support available includes:
- Transfer certificates and school recommendations
- Information about schools at new location
- Educational allowance continuity
- Admission assistance through organization contacts

## Special Circumstances

### Q22: Can couples working in same organization get joint transfer?
**A:** Yes, joint transfers are facilitated for:
- Both spouses working in same organization
- Coordinated posting to same location/nearby locations
- Subject to administrative feasibility and position availability

### Q23: What about transfer during pregnancy or with newborn?
**A:** Special provisions include:
- Deferment of transfer until after maternity leave
- Medical support during travel
- Extended joining time if required
- Priority accommodation for family needs

### Q24: Can I get transfer for child's higher education?
**A:** Transfer may be considered for:
- Child's admission to premier institutions
- Special educational needs
- Medical education requirements
- Subject to organizational requirements and availability

## Mutual Transfer

### Q25: How does mutual transfer work?
**A:** Mutual transfer process:
1. Both employees agree to exchange postings
2. Joint application with both signatures
3. Both departments must approve
4. Simultaneous transfer orders issued
5. Coordinated relieving and joining

### Q26: What if one person backs out of mutual transfer?
**A:** If mutual transfer is withdrawn:
- Both employees return to original positions
- No penalty if withdrawal before approval
- Administrative action if withdrawal after orders issued

## Appeals and Grievances

### Q27: How can I appeal a transfer decision?
**A:** Appeal process:
1. First appeal to immediate higher authority (30 days)
2. Second appeal to departmental head (30 days)
3. Final appeal to transfer review committee
4. Administrative tribunal (if applicable)

### Q28: What is the transfer review committee?
**A:** The committee comprises:
- Senior administrative officer (Chairman)
- HR representative
- Medical officer (for medical cases)
- Employee representative
- Subject expert (as required)

## Recent Updates (2024)

### Q29: What are the new transfer policy changes for 2024?
**A:** Recent updates include:
- Digital application system
- Faster processing timelines
- Enhanced spouse ground provisions
- Improved appeal mechanisms
- Better coordination between departments

### Q30: Is there an online system for transfer applications?
**A:** Yes, the new Transfer Management System (TMS) offers:
- Online application submission
- Document upload facility
- Status tracking
- Automated notifications
- Digital approvals

## Contact Information

### Transfer Related Queries
- **Transfer Section:** transfer@apex.gov.in
- **Helpline:** 1800-XXX-TRANSFER
- **Online Portal:** portal.apex.gov.in/transfers

### Specific Support
- **Spouse Ground Transfers:** spouse-transfer@apex.gov.in
- **Medical Ground Transfers:** medical-transfer@apex.gov.in
- **Appeals and Grievances:** appeals@apex.gov.in

---

*This FAQ is updated regularly. For the most current information, please check the official transfer policy document or contact the transfer section.*
    `
  },
  '6': {
    id: '6',
    title: 'New Initiatives for Women Scientists Announced',
    summary: 'Government announces new initiatives including mentorship programs and career advancement opportunities.',
    category: 'news',
    type: 'news',
    readTime: '5 min read',
    publishDate: '2024-02-20',
    lastUpdated: '2024-02-20',
    author: 'News Team',
    authorRole: 'APEX Communications',
    views: 321,
    rating: 4.4,
    tags: ['Women in Science', 'Government Initiatives', 'Career Development', 'STEM'],
    relatedResources: ['3', '1', '2'],
    content: `
# New Initiatives for Women Scientists Announced

## Major Government Initiative Launched

The Government of India, in collaboration with leading scientific institutions, has announced a comprehensive set of initiatives aimed at enhancing opportunities for women scientists and researchers across the country. These programs represent a significant investment in gender equality within the scientific community and address long-standing challenges faced by women in STEM fields.

## Key Initiatives Overview

### 1. Women Scientists Excellence Program (WSEP)
A flagship initiative with ₹500 crores funding over 5 years to support women scientists at various career stages.

**Key Features:**
- Research grants up to ₹50 lakhs per project
- Career advancement fellowships
- International collaboration opportunities
- Industry partnership programs

### 2. Mentorship and Leadership Development
Comprehensive mentorship network connecting senior women scientists with emerging talent.

**Components:**
- One-on-one mentoring relationships
- Group mentoring circles
- Leadership workshops and training
- Cross-institutional networking events

### 3. Work-Life Balance Support Systems
Enhanced policies and infrastructure to support women scientists' dual responsibilities.

**Provisions:**
- Flexible working arrangements
- Enhanced childcare facilities
- Career break re-entry programs
- Family support services

## Detailed Program Descriptions

### Women Scientists Excellence Program (WSEP)

#### Research Grants
- **Early Career Grants:** ₹10-15 lakhs for researchers with 0-5 years experience
- **Mid-Career Grants:** ₹25-35 lakhs for researchers with 5-15 years experience
- **Senior Research Grants:** ₹40-50 lakhs for established researchers
- **Collaborative Research Grants:** Up to ₹75 lakhs for multi-institutional projects

#### Eligibility Criteria
- Indian citizen or overseas citizen of Indian origin
- PhD in relevant scientific discipline
- Affiliated with recognized research institution
- Demonstrated research potential and track record

#### Application Process
- Online application through dedicated portal
- Peer review by international experts
- Interview process for shortlisted candidates
- Rolling applications throughout the year

### Mentorship Network Initiative

#### Mentor Categories
1. **Research Mentors:** Senior scientists providing technical guidance
2. **Career Mentors:** Leaders offering career development advice
3. **Industry Mentors:** Professionals bridging academia-industry gap
4. **International Mentors:** Global experts providing global perspectives

#### Mentee Support
- Structured mentoring programs (6-12 months)
- Regular interaction sessions
- Progress tracking and evaluation
- Resource sharing and networking opportunities

#### Success Metrics
- Career advancement of mentees
- Research productivity improvements
- Leadership role achievements
- International collaboration development

### Infrastructure and Facility Enhancements

#### Childcare Support
- **On-site Crèches:** Professional childcare at all major research institutions
- **Emergency Childcare:** Backup services for unexpected situations
- **School Holiday Programs:** Special arrangements during school breaks
- **Lactation Facilities:** Private, comfortable nursing rooms

#### Technology Support
- **Remote Work Infrastructure:** Advanced communication and collaboration tools
- **Mobile Laboratory Access:** Flexible access to research facilities
- **Digital Resource Libraries:** Online access to scientific literature and databases
- **Virtual Conference Participation:** Support for remote participation in scientific events

## Specific Focus Areas

### Breaking the Glass Ceiling
Addressing systemic barriers that prevent women from reaching leadership positions in science.

**Initiatives:**
- Leadership development programs
- Bias awareness training for hiring committees
- Transparent promotion processes
- Gender-balanced selection panels

### Encouraging Young Women in STEM
Early intervention programs to inspire and support young women entering scientific careers.

**Programs:**
- School outreach initiatives
- Science fair competitions
- Summer research internships
- Scholarship programs for undergraduate studies

### Supporting Career Transitions
Assistance for women returning to science after career breaks or transitioning between fields.

**Support Includes:**
- Re-entry fellowships
- Skill update programs
- Networking opportunities
- Gradual workload increase options

## Implementation Timeline

### Phase 1 (April 2024 - March 2025)
- Launch of WSEP grant applications
- Establishment of mentorship network
- Infrastructure development at premier institutions
- Baseline assessment of current women scientists

### Phase 2 (April 2025 - March 2027)
- Expansion to Tier-2 institutions
- International collaboration development
- Industry partnership establishment
- Mid-term evaluation and course correction

### Phase 3 (April 2027 - March 2029)
- Full-scale implementation across all institutions
- Impact assessment and documentation
- Policy recommendations for future
- Sustainability planning

## Expected Outcomes

### Quantitative Targets
- **30% increase** in women scientists in senior positions by 2029
- **500+ women researchers** supported through WSEP grants
- **1000+ mentoring relationships** established
- **50+ new research projects** led by women scientists

### Qualitative Improvements
- Enhanced work-life balance satisfaction
- Improved retention rates in scientific careers
- Increased international visibility of Indian women scientists
- Cultural shift towards gender equality in research institutions

## Success Stories and Testimonials

### Dr. Meera Patel, Biotechnology Researcher
*"The early career grant allowed me to establish my own research lab and pursue my passion for cancer research. The mentorship program connected me with international collaborators who have been instrumental in my growth."*

### Prof. Kavya Krishnan, Physics Department Head
*"The leadership development program gave me the confidence and skills to take on administrative responsibilities while continuing my research. It's empowering to see systematic support for women in science."*

### Dr. Anita Sharma, Environmental Scientist
*"After a 3-year career break for family reasons, the re-entry fellowship helped me get back into research. The flexible working arrangements make it possible to balance my responsibilities as a mother and scientist."*

## Global Context and Comparisons

### International Benchmarks
- **Nordic Countries:** 40-45% women in senior scientific positions
- **European Union:** Target of 40% women in research leadership by 2030
- **United States:** NSF initiatives supporting women in STEM
- **Australia:** SAGE (Science in Australia Gender Equity) initiative

### India's Position
- **Current Status:** 25% women in scientific positions, 15% in leadership roles
- **Growth Trend:** 3% annual increase over past 5 years
- **Future Projection:** Target of 35% women in science by 2030

## Industry Partnerships

### Private Sector Collaboration
Leading companies have committed to supporting these initiatives:

- **Technology Sector:** Infosys, TCS, Wipro providing industry mentorship
- **Pharmaceutical Companies:** Dr. Reddy's, Cipla offering research collaborations
- **Biotechnology Firms:** Biocon, Serum Institute providing career opportunities
- **Energy Sector:** ONGC, NTPC supporting environmental research

### International Organizations
- **UNESCO:** Technical assistance and global best practices sharing
- **UN Women:** Policy guidance and advocacy support
- **World Bank:** Financial and strategic support
- **L'Oréal Foundation:** Research grants and recognition programs

## Challenges and Mitigation Strategies

### Implementation Challenges
1. **Institutional Resistance:** Traditional mindsets and practices
2. **Resource Constraints:** Limited funding and infrastructure
3. **Geographic Disparities:** Urban-rural divide in opportunities
4. **Cultural Barriers:** Societal expectations and gender roles

### Mitigation Approaches
- **Change Management:** Comprehensive training and awareness programs
- **Resource Mobilization:** Public-private partnerships and international funding
- **Decentralized Implementation:** Regional centers and satellite programs
- **Cultural Sensitivity:** Community engagement and stakeholder involvement

## Monitoring and Evaluation

### Key Performance Indicators
- **Participation Rates:** Number of women applying and benefiting from programs
- **Career Progression:** Promotion rates and leadership positions achieved
- **Research Output:** Publications, patents, and innovations by program participants
- **Satisfaction Metrics:** Feedback from beneficiaries and stakeholders

### Evaluation Framework
- **Quarterly Reviews:** Progress assessment and course correction
- **Annual Impact Assessment:** Comprehensive evaluation of outcomes
- **External Evaluation:** Independent assessment by international experts
- **Longitudinal Studies:** Long-term career tracking of program participants

## Future Vision

### 2030 Goals
- **Gender Parity:** Equal representation in scientific research
- **Global Recognition:** India as a leader in women-in-science initiatives
- **Innovation Excellence:** Women-led breakthrough discoveries and innovations
- **Sustainable Ecosystem:** Self-sustaining support systems for women scientists

### Beyond 2030
- **Leadership Export:** Indian women scientists leading global initiatives
- **Policy Influence:** India's model adopted by other developing countries
- **Scientific Diplomacy:** Women scientists as ambassadors of international cooperation
- **Social Impact:** Science-led solutions to gender equality challenges

## How to Participate

### For Aspiring Applicants
1. **Check Eligibility:** Review criteria for relevant programs
2. **Prepare Application:** Gather required documents and references
3. **Submit Online:** Use dedicated portal for applications
4. **Follow Up:** Track application status and respond to queries

### For Institutions
1. **Registration:** Enroll as participating institution
2. **Infrastructure:** Develop required facilities and support systems
3. **Implementation:** Execute programs according to guidelines
4. **Reporting:** Submit regular progress and impact reports

### For Mentors
1. **Volunteer:** Express interest in mentoring through portal
2. **Training:** Complete mentor certification program
3. **Matching:** Get paired with suitable mentees
4. **Engagement:** Maintain regular interaction and support

## Contact Information

### Program Coordination
- **National Coordinator:** Dr. Sunita Verma, Secretary, DST
- **Email:** women-scientists@dst.gov.in
- **Phone:** +91-11-2567-XXXX
- **Website:** www.women-scientists-initiative.gov.in

### Regional Coordinators
- **North Zone:** Dr. Priya Sharma (IIT Delhi)
- **South Zone:** Dr. Lakshmi Rao (IISc Bangalore)
- **East Zone:** Dr. Mallika Sen (IIT Kharagpur)
- **West Zone:** Dr. Kavita Patel (IIT Bombay)

### Support Services
- **Technical Helpline:** 1800-XXX-WOMEN
- **Email Support:** support@women-scientists.gov.in
- **Social Media:** @WomenScientistsIndia

---

*This initiative represents a historic commitment to gender equality in Indian science. Together, we can build a more inclusive and innovative scientific community.*
    `
  }
}

export default function ResourceDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [resource, setResource] = useState<ResourceContent | null>(null)
  const [isBookmarked, setIsBookmarked] = useState(false)
  const [relatedResources, setRelatedResources] = useState<ResourceContent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const resourceId = params.resourceId as string
    const resourceData = resourcesContent[resourceId]
    
    if (!resourceData) {
      router.push('/resources')
      return
    }

    setResource(resourceData)
    
    // Load related resources
    const related = resourceData.relatedResources
      .map(id => resourcesContent[id])
      .filter(Boolean)
    setRelatedResources(related)
    
    // Check if bookmarked (from localStorage)
    const bookmarks = JSON.parse(localStorage.getItem('bookmarked_resources') || '[]')
    setIsBookmarked(bookmarks.includes(resourceId))
    
    setLoading(false)
  }, [params.resourceId, router])

  const toggleBookmark = () => {
    const resourceId = params.resourceId as string
    const bookmarks = JSON.parse(localStorage.getItem('bookmarked_resources') || '[]')
    
    if (isBookmarked) {
      const newBookmarks = bookmarks.filter((id: string) => id !== resourceId)
      localStorage.setItem('bookmarked_resources', JSON.stringify(newBookmarks))
      setIsBookmarked(false)
    } else {
      const newBookmarks = [...bookmarks, resourceId]
      localStorage.setItem('bookmarked_resources', JSON.stringify(newBookmarks))
      setIsBookmarked(true)
    }
  }

  const handleShare = async () => {
    const url = window.location.href
    const title = resource?.title || 'APEX Resource'
    
    if (navigator.share) {
      try {
        await navigator.share({ title, url })
      } catch (error) {
        // Fallback to clipboard
        navigator.clipboard.writeText(url)
        alert('Link copied to clipboard!')
      }
    } else {
      navigator.clipboard.writeText(url)
      alert('Link copied to clipboard!')
    }
  }

  const handlePrint = () => {
    window.print()
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'policy': return 'bg-blue-100 text-blue-800'
      case 'guide': return 'bg-green-100 text-green-800'
      case 'story': return 'bg-purple-100 text-purple-800'
      case 'faq': return 'bg-yellow-100 text-yellow-800'
      case 'news': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-12 bg-gray-200 rounded w-3/4 mb-8"></div>
          <div className="space-y-4">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!resource) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Resource Not Found</h1>
          <p className="text-gray-600 mb-4">The requested resource could not be found.</p>
          <Link href="/resources">
            <Button>
              <ArrowLeftIcon className="h-4 w-4 mr-2" />
              Back to Resources
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <Link href="/resources" className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4">
          <ArrowLeftIcon className="h-4 w-4 mr-1" />
          Back to Resources
        </Link>
        
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-6">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-3">
              <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${getTypeColor(resource.type)}`}>
                {resource.type}
              </span>
              {resource.isFeatured && (
                <span className="text-sm bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                  Featured
                </span>
              )}
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{resource.title}</h1>
            <p className="text-lg text-gray-600 mb-4">{resource.summary}</p>
          </div>
        </div>

        {/* Meta Information */}
        <div className="flex flex-wrap items-center gap-6 text-sm text-gray-500 mb-6">
          <div className="flex items-center">
            <UserIcon className="h-4 w-4 mr-1" />
            {resource.author} • {resource.authorRole}
          </div>
          <div className="flex items-center">
            <CalendarIcon className="h-4 w-4 mr-1" />
            {new Date(resource.publishDate).toLocaleDateString()}
          </div>
          <div className="flex items-center">
            <ClockIcon className="h-4 w-4 mr-1" />
            {resource.readTime}
          </div>
          <div className="flex items-center">
            <EyeIcon className="h-4 w-4 mr-1" />
            {resource.views} views
          </div>
          <div className="flex items-center">
            <StarIcon className="h-4 w-4 mr-1 fill-current text-yellow-500" />
            {resource.rating}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3 mb-8">
          <Button variant="outline" onClick={toggleBookmark}>
            <BookmarkIcon className={`h-4 w-4 mr-2 ${isBookmarked ? 'fill-current' : ''}`} />
            {isBookmarked ? 'Bookmarked' : 'Bookmark'}
          </Button>
          <Button variant="outline" onClick={handleShare}>
            <ShareIcon className="h-4 w-4 mr-2" />
            Share
          </Button>
          <Button variant="outline" onClick={handlePrint}>
            <PrinterIcon className="h-4 w-4 mr-2" />
            Print
          </Button>
        </div>
      </div>

      {/* Content */}
      <Card className="mb-8">
        <CardContent className="p-8">
          <div className="prose max-w-none">
            <div 
              className="text-gray-800 leading-relaxed"
              dangerouslySetInnerHTML={{ 
                __html: resource.content
                  .replace(/\n/g, '<br>')
                  .replace(/#{3,}\s*(.+)/g, '<h3 class="text-lg font-semibold mt-6 mb-3 text-gray-900">$1</h3>')
                  .replace(/#{2}\s*(.+)/g, '<h2 class="text-xl font-semibold mt-8 mb-4 text-gray-900">$1</h2>')
                  .replace(/#{1}\s*(.+)/g, '<h1 class="text-2xl font-bold mt-8 mb-6 text-gray-900">$1</h1>')
                  .replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold">$1</strong>')
                  .replace(/\*(.+?)\*/g, '<em>$1</em>')
                  .replace(/^- (.+)/gm, '<ul class="list-disc pl-6 my-2"><li>$1</li></ul>')
                  .replace(/(<\/ul>\s*<ul[^>]*>)/g, '')
                  .replace(/^(\d+)\.\s(.+)/gm, '<ol class="list-decimal pl-6 my-2"><li>$2</li></ol>')
                  .replace(/(<\/ol>\s*<ol[^>]*>)/g, '')
              }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Tags */}
      {resource.tags.length > 0 && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-lg">Tags</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {resource.tags.map(tag => (
                <span 
                  key={tag}
                  className="inline-flex px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Related Resources */}
      {relatedResources.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Related Resources</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {relatedResources.map(relatedResource => (
                <Link 
                  key={relatedResource.id}
                  href={`/resources/${relatedResource.id}`}
                  className="block p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:shadow-md transition-all"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(relatedResource.type)}`}>
                          {relatedResource.type}
                        </span>
                      </div>
                      <h3 className="font-medium text-gray-900 mb-1">{relatedResource.title}</h3>
                      <p className="text-sm text-gray-600 mb-2">{relatedResource.summary}</p>
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>{relatedResource.readTime}</span>
                        <span>{relatedResource.views} views</span>
                        <span>★ {relatedResource.rating}</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}