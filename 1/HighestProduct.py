#Given a list of integers, this method returns the highest product between 3 of those numbers.
#If the list has fewer than three integers, the method returns the product of all of the elements in the list.

def highestProduct(intList):
	negativeList = []
	positiveList = []
	for integer in sorted(intList):
		if integer < 0:
			negativeList.append(integer)
		else:
			positiveList.append(integer)
	
	#We make sure that each part of the split list is sorted in decending order with regards to the absolute value of the elements.
	positiveList = list(reversed(positiveList))
	
	#We cannot just assume that the three highest factors will give the highest product.
	if len(positiveList) >= 3:
		
		#We consider the posibility that the product of the two lowest negative integers is higher than the product of the second and third highest positive integers.
		if len(negativeList) >= 2 and negativeList[0]*negativeList[1] > positiveList[1]*positiveList[2]:
				return positiveList[0]*negativeList[0]*negativeList[1]
		
		#The highest product is accomplished only with positive factors.
		else:
			return positiveList[0]*positiveList[1]*positiveList[2]
	
	#If there are only one or two positive factors, a product of three integers has to include at least one negative factor. 
	if len(positiveList) >= 1:
		
		#If at least one factor has to be negative, it's preferable that two factors are negative.
		if (len(negativeList)>=2):
			return positiveList[0]*negativeList[0]*negativeList[1]
		
		#If there is only one or zero negative factors available, we have no choice but to multiply the available negative factors with our positive factor. 
		else:
			product = positiveList[0]
			for integer in list(reversed(negativeList))[0:2]:
				product*=integer
			return product


	#If there are no positive factors available, the product will be negative.
	#Therefore, we multiply the three negative factors with the lowest absolute value.
	#If there are not three negative factors available, we still have no choice but to multiply all negative factors available.	
	else:
		product = 1
		for integer in list(reversed(negativeList))[0:3]:
			product*=integer
		return product

print(highestProduct([1, 10, 2, 6, 5, 3])) #Should return 300
print(highestProduct([-1, -10, -2, -6, -5, -3])) #Should return -6
print(highestProduct([1])) #Should return 1
print(highestProduct([-1])) #Should return -1
print(highestProduct([])) #Should return 1
print(highestProduct([5, -3, -15, -1])) #Should return 225
print(highestProduct([10, 3, 5, 6, 20]))
print(highestProduct([-10, -3, -5, -6, -20])) #Should return -90
print(highestProduct([1, -4, 3, -6, 7, 0])) #Should return 168
print(highestProduct([1, 4, 3, -6, -7, 0])) #Should return 168
print(highestProduct([1, 2, -3, -4])) #Should return 24