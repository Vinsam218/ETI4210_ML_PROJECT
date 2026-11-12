/**
 * Creates the "Student Learning Habits and Academic Performance Survey" as a REAL Google Form,
 * plus a linked Google Sheet for responses.
 *
 * HOW TO RUN (about 2 minutes):
 *  1. Go to https://script.google.com and click "New project" (signed in to the Google account that should own the form).
 *  2. Delete the sample code, paste this whole file, click Save.
 *  3. Choose the function  createSurveyForm  in the toolbar and click Run. Approve the permission prompts
 *     (it needs Forms and Sheets access to YOUR account only).
 *  4. Open View > Logs (or Execution log): it prints the Editor URL, the Respondent URL and the Sheet URL.
 *  5. Open the Respondent URL in a private/incognito window, submit ONE test answer, confirm it appears in the Sheet,
 *     then delete that test row before real data collection starts.
 *
 * Generated from form_spec.json; edit the SPEC below to change questions.
 */
const SPEC = {
 "title": "Student Learning Habits and Academic Performance Survey",
 "description": "This questionnaire investigates the relationship between university students' learning habits, academic experiences and academic performance. The information collected will be used for academic research into machine-learning-based classification of student academic performance. Participation is voluntary. No names, registration numbers, telephone numbers or personal email addresses should be collected.",
 "questions": [
  {
   "sec": "A",
   "secname": "Student Background",
   "id": "A1",
   "var": "university",
   "text": "1. Which university do you attend?",
   "type": "dropdown",
   "opts": [
    "University of Nairobi",
    "Kenyatta University",
    "Moi University",
    "Jomo Kenyatta University of Agriculture and Technology",
    "Egerton University",
    "Maseno University",
    "Technical University of Kenya",
    "Dedan Kimathi University of Technology",
    "Masinde Muliro University of Science and Technology",
    "Multimedia University of Kenya",
    "Strathmore University",
    "United States International University-Africa",
    "Mount Kenya University",
    "Daystar University",
    "Catholic University of Eastern Africa",
    "KCA University",
    "Africa Nazarene University",
    "Kabarak University",
    "Other (please specify in the next question)"
   ],
   "req": true
  },
  {
   "sec": "A",
   "id": "A1b",
   "var": "university_other",
   "text": "1b. If you chose 'Other', please type the name of your university.",
   "type": "text",
   "req": false
  },
  {
   "sec": "A",
   "id": "A2",
   "var": "programme",
   "text": "2. What is your academic programme or field of study?",
   "type": "dropdown",
   "opts": [
    "BSc Computer Science",
    "BSc Information Technology",
    "Bachelor of Business Information Technology",
    "Bachelor of Commerce",
    "BA Economics",
    "BSc Statistics and Data Science",
    "BSc Mathematics",
    "BSc Nursing",
    "Bachelor of Medicine and Surgery (MBChB)",
    "Bachelor of Education (Arts)",
    "Bachelor of Education (Science)",
    "BSc Civil Engineering",
    "BSc Electrical and Electronic Engineering",
    "Bachelor of Laws (LLB)",
    "BSc Agriculture",
    "BA Journalism and Mass Communication",
    "BSc Biochemistry",
    "Other (please specify in the next question)"
   ],
   "req": true
  },
  {
   "sec": "A",
   "id": "A2b",
   "var": "programme_other",
   "text": "2b. If you chose 'Other', please type your programme.",
   "type": "text",
   "req": false
  },
  {
   "sec": "A",
   "id": "A3",
   "var": "year_of_study",
   "text": "3. What is your current year of study?",
   "type": "mc",
   "opts": [
    "First year",
    "Second year",
    "Third year",
    "Fourth year",
    "Fifth year",
    "Other"
   ],
   "req": true
  },
  {
   "sec": "A",
   "id": "A4",
   "var": "mode_of_study",
   "text": "4. What is your mode of study?",
   "type": "mc",
   "opts": [
    "Full-time",
    "Part-time",
    "Distance learning",
    "Blended learning"
   ],
   "req": true
  },
  {
   "sec": "A",
   "id": "A5",
   "var": "semester",
   "text": "5. Which academic semester are you currently in?",
   "type": "dropdown",
   "opts": [
    "Semester 1",
    "Semester 2",
    "Semester 3 / Summer",
    "Trimester 1",
    "Trimester 2",
    "Trimester 3",
    "Other"
   ],
   "req": true
  },
  {
   "sec": "B",
   "secname": "Study Habits",
   "id": "B6",
   "var": "study_hours_weekly",
   "text": "6. Approximately how many hours do you spend studying independently per week (outside lectures)?",
   "type": "number",
   "lo": 0,
   "hi": 80,
   "help": "Enter a whole number of hours, 0-80.",
   "req": true
  },
  {
   "sec": "B",
   "id": "B7",
   "var": "timetable_frequency",
   "text": "7. How frequently do you follow a personal study timetable?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "B",
   "id": "B8",
   "var": "study_location",
   "text": "8. What is your preferred study location?",
   "type": "mc",
   "opts": [
    "Home",
    "University library",
    "Hostel",
    "Classroom",
    "Group study area",
    "Other"
   ],
   "req": true
  },
  {
   "sec": "B",
   "id": "B9",
   "var": "group_discussion_frequency",
   "text": "9. How frequently do you participate in group discussions?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "B",
   "id": "B10",
   "var": "revision_frequency",
   "text": "10. How often do you revise notes outside scheduled lecture hours?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "C",
   "secname": "Class Attendance",
   "id": "C11",
   "var": "attendance_percentage",
   "text": "11. What percentage of scheduled lectures do you typically attend?",
   "type": "number",
   "lo": 0,
   "hi": 100,
   "help": "Enter a number from 0 to 100 (no % sign).",
   "req": true
  },
  {
   "sec": "C",
   "id": "C12",
   "var": "missed_lecture_reasons",
   "text": "12. What are the main reasons for missing lectures? (select all that apply)",
   "type": "checkbox",
   "opts": [
    "I rarely miss lectures",
    "Illness",
    "Transport or distance",
    "Financial difficulties",
    "Work or family responsibilities",
    "Lecturer absent or classes cancelled",
    "Overlapping timetable",
    "Lack of motivation",
    "Poor sleep or fatigue"
   ],
   "other": true,
   "req": true
  },
  {
   "sec": "C",
   "id": "C13",
   "var": "lab_attendance",
   "text": "13. How frequently do you attend laboratory sessions or practical classes?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always",
    "Not applicable to my programme"
   ],
   "req": true
  },
  {
   "sec": "D",
   "secname": "Assignment Completion",
   "id": "D14",
   "var": "assignment_completion_percentage",
   "text": "14. What percentage of assignments do you submit before the deadline?",
   "type": "number",
   "lo": 0,
   "hi": 100,
   "help": "Enter a number from 0 to 100 (no % sign).",
   "req": true
  },
  {
   "sec": "D",
   "id": "D15",
   "var": "independent_assignment_frequency",
   "text": "15. How frequently do you complete assignments independently?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "D",
   "id": "D16",
   "var": "help_seeking_frequency",
   "text": "16. How often do you seek academic assistance when experiencing difficulties?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "E",
   "secname": "Sleep and Lifestyle",
   "id": "E17",
   "var": "sleep_hours",
   "text": "17. On average, how many hours do you sleep per night?",
   "type": "number",
   "lo": 2,
   "hi": 14,
   "help": "You may use one decimal place, e.g. 6.5.",
   "req": true
  },
  {
   "sec": "E",
   "id": "E18",
   "var": "sleep_consistency",
   "text": "18. How would you describe your sleep consistency?",
   "type": "mc",
   "opts": [
    "Very consistent",
    "Mostly consistent",
    "Somewhat irregular",
    "Very irregular"
   ],
   "req": true
  },
  {
   "sec": "E",
   "id": "E19",
   "var": "sleep_concentration_difficulty",
   "text": "19. How frequently do you have difficulty concentrating during lectures because of inadequate sleep?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "F",
   "secname": "Internet and Learning Resources",
   "id": "F20",
   "var": "internet_access",
   "text": "20. Do you have reliable internet access for academic activities?",
   "type": "mc",
   "opts": [
    "Yes",
    "No"
   ],
   "req": true
  },
  {
   "sec": "F",
   "id": "F21",
   "var": "internet_method",
   "text": "21. What is your primary internet access method?",
   "type": "mc",
   "opts": [
    "Home Wi-Fi / fibre",
    "University Wi-Fi",
    "Mobile data bundles",
    "Cyber cafe / public hotspot",
    "Other"
   ],
   "req": true
  },
  {
   "sec": "F",
   "id": "F22",
   "var": "online_resource_frequency",
   "text": "22. How frequently do you use online academic resources (e-books, journals, e-learning platforms)?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "F",
   "id": "F23",
   "var": "learning_material_access_rating",
   "text": "23. How would you rate your access to learning materials?",
   "type": "scale",
   "lo": 1,
   "hi": 5,
   "lolabel": "Very poor",
   "hilabel": "Excellent",
   "req": true
  },
  {
   "sec": "G",
   "secname": "Social Media and Digital Behaviour",
   "id": "G24",
   "var": "social_media_hours_daily",
   "text": "24. Approximately how many hours per day do you spend on social media?",
   "type": "number",
   "lo": 0,
   "hi": 16,
   "help": "You may use one decimal place, e.g. 2.5.",
   "req": true
  },
  {
   "sec": "G",
   "id": "G25",
   "var": "social_media_interruption",
   "text": "25. How frequently does social media interrupt your study sessions?",
   "type": "mc",
   "opts": [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Always"
   ],
   "req": true
  },
  {
   "sec": "G",
   "id": "G26",
   "var": "platforms_used",
   "text": "26. Which digital platforms do you use most frequently? (select all that apply)",
   "type": "checkbox",
   "opts": [
    "WhatsApp",
    "TikTok",
    "Instagram",
    "Facebook",
    "X (Twitter)",
    "YouTube",
    "Snapchat",
    "Telegram",
    "LinkedIn"
   ],
   "other": true,
   "req": true
  },
  {
   "sec": "H",
   "secname": "Previous Academic Performance",
   "id": "H27a",
   "var": "prev_score_scale",
   "text": "27a. This section is about the semester BEFORE your most recently completed semester. Which format will you use to report that semester's result?",
   "type": "mc",
   "opts": [
    "Percentage mean score (e.g. 63%)",
    "GPA out of 4.0",
    "GPA out of 5.0",
    "Other / not sure"
   ],
   "req": true
  },
  {
   "sec": "H",
   "id": "H27",
   "var": "previous_performance",
   "text": "27. What was your approximate academic average or GPA in that earlier semester (the one before your most recently completed semester)?",
   "type": "number",
   "lo": 0,
   "hi": 100,
   "help": "Enter the value in the format chosen above (e.g. 64 for a percentage, 3.2 for a GPA).",
   "req": true
  },
  {
   "sec": "H",
   "id": "H28",
   "var": "previous_performance_self_rating",
   "text": "28. How would you describe your performance in that earlier semester?",
   "type": "mc",
   "opts": [
    "Excellent",
    "Good",
    "Average",
    "Below average",
    "Poor"
   ],
   "req": true
  },
  {
   "sec": "H",
   "id": "H29",
   "var": "performance_change",
   "text": "29. Compared with that earlier semester, has your performance in your most recently completed semester changed significantly?",
   "type": "mc",
   "opts": [
    "Improved significantly",
    "Improved slightly",
    "About the same",
    "Declined slightly",
    "Declined significantly"
   ],
   "req": true
  },
  {
   "sec": "I",
   "secname": "Academic Performance (Target Variable)",
   "id": "I30a",
   "var": "current_score_scale",
   "text": "30a. Which format will you use to report your most recently completed semester's result? (Use the same format as question 27a if possible.)",
   "type": "mc",
   "opts": [
    "Percentage mean score (e.g. 63%)",
    "GPA out of 4.0",
    "GPA out of 5.0",
    "Other / not sure"
   ],
   "req": true
  },
  {
   "sec": "I",
   "id": "I30",
   "var": "current_performance",
   "text": "30. What was your approximate academic average or GPA in your most recently completed semester?",
   "type": "number",
   "lo": 0,
   "hi": 100,
   "help": "Enter the value in the format chosen above (e.g. 58 for a percentage, 3.0 for a GPA).",
   "req": true
  },
  {
   "sec": "I",
   "id": "I30b",
   "var": "current_performance_band",
   "text": "30b. Which band best matches your most recently completed semester's overall average? (If you reported a GPA, choose the band your university would map it to.)",
   "type": "mc",
   "opts": [
    "70% and above (A / First Class Honours)",
    "60-69% (B / Upper Second Class)",
    "50-59% (C / Lower Second Class)",
    "40-49% (D / Pass)",
    "Below 40% (E / Fail)"
   ],
   "req": true
  },
  {
   "sec": "I",
   "id": "I30c",
   "var": "grading_system_note",
   "text": "30c. (Optional) If your university uses a different grading scale from those above, describe it briefly (e.g. 'CGPA 4.0: 3.5+ = First Class').",
   "type": "text",
   "req": false
  }
 ]
};

function createSurveyForm() {
  const form = FormApp.create(SPEC.title);
  form.setDescription(SPEC.description);
  form.setCollectEmail(false);               // never collect email addresses automatically
  form.setAllowResponseEdits(false);
  form.setLimitOneResponsePerUser(false);    // avoids forcing a Google sign-in (keeps responses anonymous)
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setPublishingSummary(true);           // respondents can see summary charts after submitting (set false if you prefer not)
  form.setConfirmationMessage('Thank you. Your anonymous response has been recorded.');
  try { form.setRequireLogin(false); } catch (e) {}   // only available on Google Workspace accounts
  try { form.setAcceptingResponses(true); } catch (e) {}
  try { if (form.setPublished) form.setPublished(true); } catch (e) {}

  let currentSection = null;
  SPEC.questions.forEach(function (q) {
    if (q.sec !== currentSection) {
      currentSection = q.sec;
      const name = q.secname || ('Section ' + q.sec);
      if (form.getItems().length > 0) {
        form.addPageBreakItem().setTitle('Section ' + q.sec + ': ' + name);
      } else {
        form.addSectionHeaderItem().setTitle('Section ' + q.sec + ': ' + name);
      }
    }
    let item;
    if (q.type === 'dropdown') {
      item = form.addListItem().setChoiceValues(q.opts);
    } else if (q.type === 'mc') {
      item = form.addMultipleChoiceItem();
      item.setChoiceValues(q.opts);
    } else if (q.type === 'checkbox') {
      item = form.addCheckboxItem();
      item.setChoiceValues(q.opts);
      if (q.other) item.showOtherOption(true);
    } else if (q.type === 'scale') {
      item = form.addScaleItem().setBounds(q.lo, q.hi).setLabels(q.lolabel, q.hilabel);
    } else if (q.type === 'number') {
      item = form.addTextItem();
      item.setValidation(FormApp.createTextValidation()
        .setHelpText('Please enter a number between ' + q.lo + ' and ' + q.hi + '.')
        .requireNumberBetween(q.lo, q.hi).build());
    } else {
      item = form.addTextItem();
    }
    item.setTitle(q.text).setRequired(!!q.req);
    if (q.help) item.setHelpText(q.help);
  });

  // Linked response spreadsheet
  const ss = SpreadsheetApp.create(SPEC.title + ' (Responses)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('EDITOR URL    : ' + form.getEditUrl());
  Logger.log('RESPONDENT URL: ' + form.getPublishedUrl());
  Logger.log('RESPONSE SHEET: ' + ss.getUrl());
}
