#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象 , bz==busy==业务函数
#【返回类型说明】 V的返回类型 == bz的返回类型 , S的类型==[bz的返回类型]
#【备注】 V == traverse.py.TraverseAbs.V,  S == traverse.py.TraverseAbs.S

import typing
from neo4j import Session
from neo4j.graph import Node
from dbConn_inject_neo4j import dbConn_inject_neo4j_default
from util_basic import assertRE_fnCallId_eq_RL__return_fnCallId, assertSonLsEmptyWhenLeaf
from util_file import readTxt
from neo4j_misc import update__init_deepth_as_null
from traverse import TraverseAbs
from neo4j_tool import neo4j_update
from util_datetime import nowDateTimeTxt


class BzWriteDeepth(TraverseAbs):

    cypher__update_setFieldDeepth=readTxt("cypher_src/update_setFieldDeepth.cypher") 

    def __init__(self, sess: Session) -> None:
        super().__init__(sess)

# 【业务函数】 计算深度 并 写deepth字段为深度值
    def bz(self, RE:Node, RL:Node, isLeaf:bool, S:typing.List[int], _)->int:

        #断言叶子的直接孩子们为空，目的是 检验本项目的其他地方逻辑是否有问题
        assertSonLsEmptyWhenLeaf(isLeaf,_)
    
        #deepth数值列表即为S
        deepth_ls:typing.List[int]= S

        #断言起点、终点fnCallId相同，目的是 检验本项目的其他地方逻辑是否有问题
        fnCallId=assertRE_fnCallId_eq_RL__return_fnCallId(RE,RL)
        
        #叶子的deepth为0,非叶子的deepth为 1+直接孩子们的deepth的最大值
        d=0 if isLeaf  else 1+max(deepth_ls)
        neo4j_update(self.N.sess,"update_setFieldDeepth",BzWriteDeepth.cypher__update_setFieldDeepth,params={"prm_fnCallId":fnCallId,"prm_deepth":d},filedName="更新记录数")
        print(f"BzWriteDeepth.bz, {nowDateTimeTxt()}, fnCallId={fnCallId}写字段deepth={d}; 第{self.Vi}次遍历")
        
        #注意此返回是必须的, 否则 遍历器traverse.py.TraverseAbs.V中的'S=[...bz()...]'将得不到返回值
        return d
    
    def clear_field(self):
        update__init_deepth_as_null(self.N.sess)






    

