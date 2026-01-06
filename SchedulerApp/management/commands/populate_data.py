from django.core.management.base import BaseCommand
from SchedulerApp.models import Room, Instructor, MeetingTime, Course, Department, Section


class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')

        # Clear existing data
        Section.objects.all().delete()
        Department.objects.all().delete()
        Course.objects.all().delete()
        MeetingTime.objects.all().delete()
        Instructor.objects.all().delete()
        Room.objects.all().delete()

        # Create Rooms
        rooms = [
            Room(r_number='R101', seating_capacity=30),
            Room(r_number='R102', seating_capacity=35),
            Room(r_number='R103', seating_capacity=40),
            Room(r_number='R201', seating_capacity=50),
            Room(r_number='R202', seating_capacity=45),
            Room(r_number='LAB1', seating_capacity=25),
            Room(r_number='LAB2', seating_capacity=30),
        ]
        Room.objects.bulk_create(rooms)
        self.stdout.write(self.style.SUCCESS(f'Created {len(rooms)} rooms'))

        # Create Instructors
        instructors = [
            Instructor(uid='I001', name='Dr. Sharma'),
            Instructor(uid='I002', name='Prof. Kumar'),
            Instructor(uid='I003', name='Dr. Patel'),
            Instructor(uid='I004', name='Prof. Reddy'),
            Instructor(uid='I005', name='Dr. Singh'),
            Instructor(uid='I006', name='Prof. Rao'),
            Instructor(uid='I007', name='Dr. Gupta'),
            Instructor(uid='I008', name='Prof. Mehta'),
        ]
        Instructor.objects.bulk_create(instructors)
        self.stdout.write(self.style.SUCCESS(f'Created {len(instructors)} instructors'))

        # Create Meeting Times
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        times = ['8:45 - 9:45', '10:00 - 11:00', '11:00 - 12:00', '1:00 - 2:00', '2:15 - 3:15']
        
        meeting_times = []
        pid_counter = 1
        for day in days:
            for time in times:
                meeting_times.append(
                    MeetingTime(pid=f'MT{pid_counter:02d}', time=time, day=day)
                )
                pid_counter += 1
        MeetingTime.objects.bulk_create(meeting_times)
        self.stdout.write(self.style.SUCCESS(f'Created {len(meeting_times)} meeting times'))

        # Create Courses
        courses_data = [
            ('CS101', 'Data Structures', '60', ['I001', 'I002']),
            ('CS102', 'Algorithms', '50', ['I002', 'I003']),
            ('CS201', 'Database Systems', '55', ['I003', 'I004']),
            ('CS202', 'Operating Systems', '50', ['I004', 'I005']),
            ('CS301', 'Computer Networks', '45', ['I005', 'I006']),
            ('CS302', 'Software Engineering', '50', ['I006', 'I007']),
            ('CS401', 'Machine Learning', '40', ['I007', 'I008']),
            ('CS402', 'Web Technologies', '55', ['I001', 'I008']),
        ]

        courses = []
        for course_num, course_name, max_students, instructor_uids in courses_data:
            course = Course.objects.create(
                course_number=course_num,
                course_name=course_name,
                max_numb_students=max_students
            )
            # Add instructors
            for uid in instructor_uids:
                instructor = Instructor.objects.get(uid=uid)
                course.instructors.add(instructor)
            courses.append(course)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))

        # Create Departments
        dept_cse = Department.objects.create(dept_name='Computer Science & Engineering')
        dept_cse.courses.add(*Course.objects.filter(course_number__startswith='CS'))

        dept_it = Department.objects.create(dept_name='Information Technology')
        dept_it.courses.add(*Course.objects.filter(course_number__in=['CS101', 'CS201', 'CS402']))

        dept_ece = Department.objects.create(dept_name='Electronics & Communication')
        
        self.stdout.write(self.style.SUCCESS('Created 3 departments'))

        # Create Sections
        sections_data = [
            ('SEC-A1', dept_cse, 3, 'CS101'),
            ('SEC-A2', dept_cse, 3, 'CS102'),
            ('SEC-B1', dept_cse, 2, 'CS201'),
            ('SEC-B2', dept_cse, 3, 'CS202'),
            ('SEC-C1', dept_it, 2, 'CS101'),
            ('SEC-C2', dept_it, 3, 'CS201'),
            ('SEC-D1', dept_cse, 2, 'CS301'),
            ('SEC-D2', dept_cse, 2, 'CS302'),
        ]

        for section_id, dept, num_classes, course_num in sections_data:
            course = Course.objects.get(course_number=course_num)
            Section.objects.create(
                section_id=section_id,
                department=dept,
                num_class_in_week=num_classes,
                course=course
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(sections_data)} sections'))
        self.stdout.write(self.style.SUCCESS('✓ All dummy data created successfully!'))
