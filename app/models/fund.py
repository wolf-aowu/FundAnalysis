from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text

from app.models.base import BaseModel


class Fund(BaseModel):
    __tablename__ = "fund"
    fund_code = Column(String(6), unique=True)
    fund_name = Column(Text)
    company_name = Column(Text)


class FundRecord(BaseModel):
    __tablename__ = "fund_record"
    fund_code = Column(String(6))
    fund_name = Column(Text)
    unit_net_asset_value = Column(Float)
    fund_id = Column(Integer, ForeignKey('fund.id'))
