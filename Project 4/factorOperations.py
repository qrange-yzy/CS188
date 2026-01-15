# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########

def joinFactors(factors: List[Factor]):
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """
    factors = list(factors)

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


    "*** YOUR CODE HERE ***"
    "*** YOUR CODE HERE ***"
    # 1. 确定新因子的变量集合
    # 新的 unconditioned 是所有输入因子 unconditioned 的并集
    # 新的 conditioned 是所有输入因子 conditioned 的并集
    new_unconditioned = set()
    new_conditioned = set()
    
    for f in factors:
        new_unconditioned = new_unconditioned.union(f.unconditionedVariables())
        new_conditioned = new_conditioned.union(f.conditionedVariables())
    
    # 【关键点】如果一个变量出现在了 unconditioned 里，它就不应该再出现在 conditioned 里
    # 比如 P(A) * P(B|A) -> 结果是 P(A, B)，A 从条件变量变成了联合变量
    new_conditioned = new_conditioned - new_unconditioned
    
    # 2. 创建新因子
    # 题目提示：variableDomainsDict 都是一样的，取第一个因子的就行
    new_factor = Factor(new_unconditioned, new_conditioned, factors[0].variableDomainsDict())
    
    # 3. 填充概率表
    # getAllPossibleAssignmentDicts() 会帮我们要遍历所有可能的变量赋值组合
    for assignment in new_factor.getAllPossibleAssignmentDicts():
        prob = 1.0
        # 对于每一个赋值，它的概率等于所有原因子在该赋值下的概率之积
        for f in factors:
            prob = prob * f.getProbability(assignment)
        
        # 设置新因子的概率
        new_factor.setProbability(assignment, prob)
        
    return new_factor
    "*** END YOUR CODE HERE ***"



########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        # 1. 确定新 Factor 的变量范围
        # 新的 unconditioned 变量集合 = 旧的集合 - 要消除的变量
        newUnconditioned = factor.unconditionedVariables().copy()
        newUnconditioned.remove(eliminationVariable)
        
        # conditioned 变量集合保持不变
        newConditioned = factor.conditionedVariables().copy()
        
        # 2. 初始化一个新的 Factor 对象
        # 传入新的变量集合和原始的域字典(DomainsDict)
        newFactor = Factor(newUnconditioned, newConditioned, factor.variableDomainsDict())
        
        # 3. 遍历原始 Factor 的所有可能赋值 (Assignment)
        # 逻辑：对于旧表中的每一行，去掉 eliminationVariable 后，加到新表中对应的行上
        for oldAssignment in factor.getAllPossibleAssignmentDicts():
            # 获取当前旧行的概率
            oldProb = factor.getProbability(oldAssignment)
            
            # 构建新行的赋值 (去掉要消除的变量)
            newAssignment = oldAssignment.copy()
            del newAssignment[eliminationVariable]
            
            # 获取新 Factor 中当前位置已有的概率值 (累加过程)
            currentNewProb = newFactor.getProbability(newAssignment)
            
            # 将旧概率加进去
            newFactor.setProbability(newAssignment, currentNewProb + oldProb)
            
        return newFactor
        "*** END YOUR CODE HERE ***"


    return eliminate

eliminate = eliminateWithCallTracking()

