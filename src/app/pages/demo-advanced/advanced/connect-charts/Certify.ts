export class Certify {

  Impacted_Key: string;
  Impacted_key_Value: string;
  column: string;
  message: string;
  row: string;
  value: BigInteger;
  

  constructor(Impacted_Key, Impacted_key_Value, column, message, row, value) {
    this.Impacted_Key = Impacted_Key;
    this.Impacted_key_Value = Impacted_key_Value;
    this.column = column;
    this.message = message;
    this.row = row;
    this.value = value; 
  }

}
