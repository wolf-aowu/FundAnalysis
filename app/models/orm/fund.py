from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text

from app.models.orm.base import BaseModel


class Fund(BaseModel):
    __tablename__ = "fund"
    fund_code = Column(String(6), unique=True, comment="基金代码")
    fund_name = Column(Text, comment="基金名称")
    company_name = Column(Text, comment="基金公司名称")


class FundRecord(BaseModel):
    __tablename__ = "fund_record"
    fund_code = Column(String(6), comment="基金代码")
    fund_name = Column(Text, comment="基金名称")
    unit_net_asset_value = Column(Float, comment="单位净值")
    fund_id = Column(Integer, ForeignKey('fund.id'), comment="关联的基金 id")
