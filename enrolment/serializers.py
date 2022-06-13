from rest_framework import serializers
from .models import *

class BranchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Branch
		fields = [
			'id',
			'name',
			'description',
			'address','suburb','state','postcode'
		]

class SchoolSerializer(serializers.ModelSerializer):
	class Meta:
		model = School
		fields = [
			'id',
			'branch',
			'name',
			'description',
			'accountname',
			'bsb',
			'accountno',
		]

class PersonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Family
		fields = [
			'id',
			'parent_type',
			'first_name',
			'last_name',
			'mobile',
            'email'
		]
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'first_name',
			'last_name',
            'email',
			'mobile'
		]

class MedicalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Medical
		fields = [
			'id',
			'dr_name',
			'address',
			'suburb',
			'state',
            'postcode',
            'telephone',
		]

class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = [
			'id',
			'first_name',
			'last_name',
			'sex',
			'residental_status',
			'mains_school_name',
			'mains_school_address',
			'mains_schoolsuburb',
            'mains_schoolstate',
			'mains_school_postcode',
		]
	medical = serializers.StringRelatedField()

class enrollmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = student_enroll
		fields = [
            'id',
			'paid',
			'school',
			'term_condition_accept',
			'declaration',
		]
  